
def get_normal_price(price: str) -> float:
    """
    Return normal python float value from Steam str price
    :param price: String price.
    :return: Float formatted price.
    """
    price = price.replace("$", "")
    if "," in price:
        # Remove "," in string (1,034.4335 => 1034.4335)
        price = price.split(",")[0] + price.split(",")[-1]
    new_price = f'{float(price):.2f}'  # Strip big float value (3.00000 => 3.00)
    return float(new_price)
