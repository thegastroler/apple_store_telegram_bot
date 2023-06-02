from typing import Optional


async def price_converter(price: int) -> str:
    if len(str(price)) > 6:
        return f"{str(price)[:-5]} {str(price)[-5:-2]}"
    return f"{str(price)[:-2]}"


async def make_order(user_id: Optional[int] = None, order: Optional[str] = None) -> str:
    if user_id:
        return f"{user_id}_1"
    return f"{int(order.split('_')[0])}_{int(order.split('_')[-1]) + 1}"