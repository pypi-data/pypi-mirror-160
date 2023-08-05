from typing import Any, Dict, List

from bson import ObjectId
from pydantic import BaseModel, Field

from fastel.cart.datastructures import CartConfig, ItemConfig, Product
from fastel.payment.utils import auto_order_number


class ProductItem(BaseModel):
    name: str
    amount: int
    price: int
    sales_amount: float
    unit_sales: float
    product: Product

    config: ItemConfig


class Checkout(CartConfig):
    id: ObjectId = Field(alias="_id")
    order_number: str = Field(default_factory=auto_order_number)
    total: int
    subtotal: int
    sales: int
    fee: int
    discount: int
    tax: int

    items: List[ProductItem]

    class Config:
        arbitrary_types_allowed = True


class Order(Checkout):
    order_id: str
    logistics: List[Dict[str, Any]] = []
    extra_items: List[Dict[str, Any]] = []
    discount_items: List[Dict[str, Any]] = []
    email_notified: bool = False
    is_custom: bool = False
    offline_account: str = ""
    offline_date: str = ""
    offline_tx: str = ""
    offline_username: str = ""
    note: str = ""
    payment_status: str = "waiting"
    payment_transaction_detail: Dict[str, Any] = {}
    payment_transaction_id: str = ""
    payment_transaction_time: str = ""
    invoice_status: str = "pending"
    invoice_detail: Dict[str, Any] = {}
    invoice_message: str = ""
    invoice_number: str = ""
