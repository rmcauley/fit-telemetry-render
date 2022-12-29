from collections import OrderedDict

import fitdecode

def get_fit_dict(path: str) -> dict:
    fitted = OrderedDict()

    with fitdecode.FitReader(path) as fit:
        i = 0
        time_created = 0
        field_defs = None
        for frame in fit:
            i += 1

            if frame.frame_type == 3:
                # Definition
                field_defs = frame.field_defs
            elif frame.frame_type == 4:
                if not time_created and frame.has_field("time_created"):
                    time_created = frame.get_value("time_created")

                if frame.has_field("position_lat"):
                    fitted[round((frame.get_value("timestamp") - time_created).total_seconds())] = {
                        f.name: frame.get_value(f.name)
                        for f in field_defs
                    }

    return fitted