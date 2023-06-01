from typing import Optional


async def price_converter(price: int) -> str:
    if len(str(price)) > 6:
        return f"{str(price)[:-5]} {str(price)[-5:-2]}"
    return f"{str(price)[:-2]}"


async def make_order_id(user_id: Optional[int] = None, order_id: Optional[str] = None) -> str:
    if user_id:
        return f"{user_id}_1"
    return f"{int(order_id.split('_')[0])}_{int(order_id.split('_')[-1]) + 1}"