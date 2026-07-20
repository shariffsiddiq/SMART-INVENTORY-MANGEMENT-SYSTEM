# Smart Inventory Management System

A simple Python and SQLite inventory management CLI application for tracking products, sales, stock purchases, and low-stock alerts.

## Features

- Admin login with default credentials: `admin` / `admin`
- Add new products with category, price, quantity, and supplier
- Sell products with stock validation and automatic quantity updates
- Purchase stock to increase inventory
- Search products by name or category
- View today's sales total
- Display top selling products
- Dashboard showing:
  - total products
  - available stock
  - low stock items
  - today's sales
  - top 5 selling products

## Getting Started

1. Install Python 3.10+.
2. Open a terminal in the project folder.
3. Run:

```bash
python inventory.py
```

4. Login using:

- Username: ``
- Password: ``

## Notes

- The application uses `inventory.db` in the same folder.
- The first run creates the database and default admin user.
- Use the menu to manage products and sales.
<img width="712" height="490" alt="Screenshot 2026-07-20 103323" src="https://github.com/user-attachments/assets/dc1e6a78-259d-4677-9328-9ab6635b3093" />


## Extending the Project

Possible additions for a portfolio-ready version:

- A web dashboard built with Flask or FastAPI
- Export reports to CSV
- Role-based access with employee vs admin privileges
- Supplier management and purchase orders
- Graphical charts for sales trends
