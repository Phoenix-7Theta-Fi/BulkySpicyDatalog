import streamlit as st
from ...utils import supabase  # Import Supabase client

# --- Streamlit Page Configuration ---
st.set_page_config(
    page_title="Ayurvedic Product Marketplace", page_icon=":shopping_cart:"
)

# --- Helper Functions ---
def fetch_products_from_supabase():
    """Fetches product data from your Supabase database."""
    # Replace with your actual table and column names
    products = (
        supabase.table("products")
        .select("*")
        .execute()
        .data
    )
    return products


def display_product(product):
    """Displays a single product card."""
    col1, col2 = st.columns([1, 2])  # Adjust column ratio as needed
    with col1:
        try: 
            st.image(product.get("image_url", "default_image.jpg"), width=150) 
        except:
            st.image("default_image.jpg", width=150)
    with col2:
        st.subheader(product.get("name", "Product Name"))
        st.write(product.get("description", "Product description."))
        st.write(f"Price: ${product.get('price', 0.00):.2f}")
        if st.button("Add to Cart"):
            add_to_cart(product)

# --- Cart Functionality --- 
def add_to_cart(product):
    """Adds a product to the cart."""
    if "cart" not in st.session_state:
        st.session_state["cart"] = []
    st.session_state["cart"].append(product)
    st.success(f"{product.get('name', 'Product')} added to cart!")

def view_cart():
    """Displays the items in the cart."""
    st.subheader("Your Cart")
    if "cart" not in st.session_state or not st.session_state["cart"]:
        st.write("Your cart is empty.")
        return

    for item in st.session_state["cart"]:
        st.write(f"- {item.get('name', 'Product')} - ${item.get('price', 0.00):.2f}")

    # Add checkout button or logic here if needed
    if st.button("Checkout"):
        st.warning("Checkout functionality is not implemented yet.")

# --- Marketplace UI ---
st.title("Ayurvedic Product Marketplace")

# --- Fetch products from Supabase ---
products = fetch_products_from_supabase()

# --- Display products ---
if products:
    for product in products:
        display_product(product)
else:
    st.warning("No products found in the database.")

# --- View Cart Section ---
view_cart() 