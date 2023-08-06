import dash


def which_fired() -> str:
    """Define witch inputs is fired.

    Returns:
        input_name: Python `str`.
    """
    ctx = dash.callback_context
    if not ctx.triggered:
        input_name = None
    else:
        input_name = ctx.triggered[0]["prop_id"].split(".")[0]

    return input_name
