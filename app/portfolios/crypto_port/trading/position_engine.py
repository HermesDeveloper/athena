def get_target_weight(regime, momentum):

    """
    Determine BTC allocation based on
    market regime + momentum
    """

    if regime == "BULL":

        if momentum > 0.03:
            return 0.80

        if momentum > 0.01:
            return 0.60

        return 0.50

    elif regime == "BEAR":

        if momentum < -0.03:
            return 0.20

        if momentum < -0.01:
            return 0.40

        return 0.50

    return 0.50