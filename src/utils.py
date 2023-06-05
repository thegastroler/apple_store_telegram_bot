from typing import Optional


async def price_converter(price: int) -> str:
    if 4 < len(str(price)) < 7:
        return f"{str(price)[:-3]} {str(price)[-3:]}"
    elif len(str(price)) >= 7:
        return f"{str(price)[:-6]} {str(price)[-6:-3]} {str(price)[-3:]}"
    return str(price)


async def make_order(user_id: Optional[int] = None, order: Optional[str] = None) -> str:
    if user_id:
        return f"{user_id}_1"
    return f"{int(order.split('_')[0])}_{int(order.split('_')[-1]) + 1}"
