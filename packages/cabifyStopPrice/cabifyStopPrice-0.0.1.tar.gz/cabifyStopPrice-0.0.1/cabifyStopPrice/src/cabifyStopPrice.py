homeDistances = {
    "fromPalmeras": 13.1,
    "fromGrego": 13.7,
    "fromDraft": 12.5,
}

patoDistances = {
    "fromPalmeras": 3.4,
    "fromGrego": 3.6,
    "fromDraft": 2.9,
}


def calculateStopPrice(total_distance, total_price, stop_distance):
    price_by_km = total_price / total_distance
    return price_by_km * stop_distance


def patoStopPriceFromPalmeras(total_price):
    return calculateStopPrice(homeDistances["fromPalmeras"],
                              total_price,
                              patoDistances["fromPalmeras"])


def patoStopPriceFromGrego(total_price):
    return calculateStopPrice(homeDistances["fromGrego"],
                              total_price,
                              patoDistances["fromGrego"])


def patoStopPriceFromDraft(total_price):
    return calculateStopPrice(homeDistances["fromDraft"],
                              total_price,
                              patoDistances["fromDraft"])