"""
Orders API routes with CRUD and bulk operations.
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid
import math

from ..database import get_db

router = APIRouter(prefix="/orders", tags=["orders"])


# Pydantic Models
class CustomerInput(BaseModel):
    name: str
    email: str
    avatar: Optional[str] = None


class Customer(BaseModel):
    name: str
    email: str
    avatar: Optional[str] = None


class OrderCreate(BaseModel):
    customer: CustomerInput
    total_amount: float
    status: str = "pending"
    payment_status: str = "unpaid"


class OrderUpdate(BaseModel):
    customer: Optional[CustomerInput] = None
    status: Optional[str] = None
    total_amount: Optional[float] = None
    payment_status: Optional[str] = None


class OrderResponse(BaseModel):
    id: str
    order_number: str
    customer: Customer
    order_date: str
    status: str
    total_amount: float
    payment_status: str
    created_at: str
    updated_at: str


class OrdersListResponse(BaseModel):
    orders: List[OrderResponse]
    total: int
    page: int
    limit: int
    total_pages: int


class OrderStats(BaseModel):
    total_orders_this_month: int
    pending_orders: int
    shipped_orders: int
    refunded_orders: int


class BulkStatusUpdate(BaseModel):
    order_ids: List[str]
    status: str


class BulkDuplicate(BaseModel):
    order_ids: List[str]


class BulkDelete(BaseModel):
    order_ids: List[str]


def row_to_order(row) -> OrderResponse:
    """Convert a database row to an OrderResponse."""
    return OrderResponse(
        id=row["id"],
        order_number=row["order_number"],
        customer=Customer(
            name=row["customer_name"],
            email=row["customer_email"],
            avatar=row["customer_avatar"]
        ),
        order_date=row["order_date"],
        status=row["status"],
        total_amount=row["total_amount"],
        payment_status=row["payment_status"],
        created_at=row["created_at"],
        updated_at=row["updated_at"]
    )


def get_next_order_number(cursor) -> str:
    """Generate the next order number."""
    cursor.execute("SELECT order_number FROM orders ORDER BY order_number DESC LIMIT 1")
    row = cursor.fetchone()
    if row:
        last_num = int(row["order_number"].replace("#ORD", ""))
        return f"#ORD{last_num + 1}"
    return "#ORD1000"


@router.get("/stats", response_model=OrderStats)
def get_order_stats():
    """Get order statistics for dashboard cards."""
    with get_db() as cursor:
        # Total orders this month (simplified - just count all for demo)
        cursor.execute("SELECT COUNT(*) as count FROM orders")
        total = cursor.fetchone()["count"]

        # Pending orders
        cursor.execute("SELECT COUNT(*) as count FROM orders WHERE status = 'pending'")
        pending = cursor.fetchone()["count"]

        # Shipped/Completed orders
        cursor.execute("SELECT COUNT(*) as count FROM orders WHERE status = 'completed'")
        shipped = cursor.fetchone()["count"]

        # Refunded orders
        cursor.execute("SELECT COUNT(*) as count FROM orders WHERE status = 'refunded'")
        refunded = cursor.fetchone()["count"]

        return OrderStats(
            total_orders_this_month=total,
            pending_orders=pending,
            shipped_orders=shipped,
            refunded_orders=refunded
        )


@router.get("", response_model=OrdersListResponse)
def get_orders(
    status: str = Query("all", description="Filter status: all, incomplete, overdue, ongoing, finished"),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
):
    """Get all orders with pagination and filtering."""
    with get_db() as cursor:
        # Build query based on status filter
        base_query = "FROM orders"
        params = []

        if status == "incomplete":
            base_query += " WHERE status = 'pending' AND payment_status = 'unpaid'"
        elif status == "overdue":
            base_query += " WHERE status = 'pending'"
        elif status == "ongoing":
            base_query += " WHERE status IN ('pending', 'completed') AND payment_status = 'unpaid'"
        elif status == "finished":
            base_query += " WHERE status = 'completed' AND payment_status = 'paid'"
        # "all" means no filter

        # Get total count
        cursor.execute(f"SELECT COUNT(*) as count {base_query}", params)
        total = cursor.fetchone()["count"]

        # Calculate pagination
        offset = (page - 1) * limit
        total_pages = math.ceil(total / limit) if total > 0 else 1

        # Get orders with pagination
        cursor.execute(
            f"SELECT * {base_query} ORDER BY order_number DESC LIMIT ? OFFSET ?",
            params + [limit, offset]
        )
        rows = cursor.fetchall()

        orders = [row_to_order(row) for row in rows]

        return OrdersListResponse(
            orders=orders,
            total=total,
            page=page,
            limit=limit,
            total_pages=total_pages
        )


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: str):
    """Get a single order by ID."""
    with get_db() as cursor:
        cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
        row = cursor.fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="Order not found")

        return row_to_order(row)


@router.post("", response_model=OrderResponse, status_code=201)
def create_order(order: OrderCreate):
    """Create a new order."""
    with get_db() as cursor:
        order_id = str(uuid.uuid4())
        order_number = get_next_order_number(cursor)
        now = datetime.utcnow().isoformat()
        order_date = datetime.utcnow().strftime("%Y-%m-%d")

        cursor.execute("""
            INSERT INTO orders (id, order_number, customer_name, customer_email, customer_avatar, order_date, status, total_amount, payment_status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            order_id,
            order_number,
            order.customer.name,
            order.customer.email,
            order.customer.avatar,
            order_date,
            order.status,
            order.total_amount,
            order.payment_status,
            now,
            now
        ))

        cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
        row = cursor.fetchone()
        return row_to_order(row)


@router.put("/{order_id}", response_model=OrderResponse)
def update_order(order_id: str, order: OrderUpdate):
    """Update an existing order."""
    with get_db() as cursor:
        # Check if order exists
        cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Order not found")

        # Build update query dynamically
        updates = []
        params = []

        if order.customer:
            if order.customer.name:
                updates.append("customer_name = ?")
                params.append(order.customer.name)
            if order.customer.email:
                updates.append("customer_email = ?")
                params.append(order.customer.email)
            if order.customer.avatar is not None:
                updates.append("customer_avatar = ?")
                params.append(order.customer.avatar)

        if order.status:
            updates.append("status = ?")
            params.append(order.status)

        if order.total_amount is not None:
            updates.append("total_amount = ?")
            params.append(order.total_amount)

        if order.payment_status:
            updates.append("payment_status = ?")
            params.append(order.payment_status)

        if updates:
            updates.append("updated_at = ?")
            params.append(datetime.utcnow().isoformat())
            params.append(order_id)

            cursor.execute(
                f"UPDATE orders SET {', '.join(updates)} WHERE id = ?",
                params
            )

        cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
        row = cursor.fetchone()
        return row_to_order(row)


@router.delete("/{order_id}", status_code=204)
def delete_order(order_id: str):
    """Delete an order."""
    with get_db() as cursor:
        cursor.execute("SELECT 1 FROM orders WHERE id = ?", (order_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Order not found")

        cursor.execute("DELETE FROM orders WHERE id = ?", (order_id,))


# Bulk Operations

@router.put("/bulk/status")
def bulk_update_status(data: BulkStatusUpdate):
    """Bulk update status for multiple orders."""
    with get_db() as cursor:
        now = datetime.utcnow().isoformat()
        updated = []

        for order_id in data.order_ids:
            cursor.execute(
                "UPDATE orders SET status = ?, updated_at = ? WHERE id = ?",
                (data.status, now, order_id)
            )
            if cursor.rowcount > 0:
                updated.append({"id": order_id, "status": data.status})

        return {
            "updated_count": len(updated),
            "orders": updated
        }


@router.post("/bulk/duplicate", status_code=201)
def bulk_duplicate(data: BulkDuplicate):
    """Duplicate multiple orders."""
    with get_db() as cursor:
        new_orders = []
        now = datetime.utcnow().isoformat()

        for order_id in data.order_ids:
            cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
            row = cursor.fetchone()

            if row:
                new_id = str(uuid.uuid4())
                new_order_number = get_next_order_number(cursor)

                cursor.execute("""
                    INSERT INTO orders (id, order_number, customer_name, customer_email, customer_avatar, order_date, status, total_amount, payment_status, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    new_id,
                    new_order_number,
                    row["customer_name"],
                    row["customer_email"],
                    row["customer_avatar"],
                    row["order_date"],
                    row["status"],
                    row["total_amount"],
                    row["payment_status"],
                    now,
                    now
                ))

                new_orders.append({
                    "id": new_id,
                    "order_number": new_order_number,
                    "original_order_id": order_id
                })

        return {
            "duplicated_count": len(new_orders),
            "new_orders": new_orders
        }


@router.delete("/bulk")
def bulk_delete(data: BulkDelete):
    """Bulk delete multiple orders."""
    with get_db() as cursor:
        deleted_ids = []

        for order_id in data.order_ids:
            cursor.execute("DELETE FROM orders WHERE id = ?", (order_id,))
            if cursor.rowcount > 0:
                deleted_ids.append(order_id)

        return {
            "deleted_count": len(deleted_ids),
            "deleted_ids": deleted_ids
        }
