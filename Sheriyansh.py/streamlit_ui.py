import streamlit as st
from pathlib import Path
import os

st.set_page_config(page_title="File Manager", page_icon="📁", layout="centered")
st.title("📁 File & Folder Manager")

# ── Helpers ──────────────────────────────────────────────────────────────────

def list_items():
    p = Path('')
    return list(p.rglob('*'))

def show_file_tree():
    items = list_items()
    if items:
        st.subheader("📂 Current Files & Folders")
        for i, item in enumerate(items, 1):
            icon = "📄" if item.is_file() else "📁"
            st.text(f"{i}. {icon} {item}")
    else:
        st.info("No files or folders found in the current directory.")

# ── Sidebar Navigation ────────────────────────────────────────────────────────

operation = st.sidebar.radio(
    "Choose Operation",
    ["🏠 Home", "➕ Create File", "📖 Read File", "✏️ Update File",
     "🗑️ Delete File", "🔤 Rename File", "📁 Create Folder", "❌ Delete Folder"]
)

# ── Pages ─────────────────────────────────────────────────────────────────────

if operation == "🏠 Home":
    st.markdown("Welcome to the **File Manager**. Select an operation from the sidebar.")
    show_file_tree()

# ── Create File ───────────────────────────────────────────────────────────────
elif operation == "➕ Create File":
    st.header("➕ Create a New File")
    show_file_tree()
    st.divider()
    file_name = st.text_input("Enter file name (e.g. notes.txt)")
    content   = st.text_area("Enter file content")
    if st.button("Create File", type="primary"):
        if not file_name:
            st.warning("Please enter a file name.")
        else:
            p = Path(file_name)
            if p.exists():
                st.error("⚠️ FILE ALREADY EXISTS!")
            else:
                with open(file_name, 'w') as f:
                    f.write(content)
                st.success(f"✅ File **{file_name}** created successfully!")
                st.rerun()

# ── Read File ─────────────────────────────────────────────────────────────────
elif operation == "📖 Read File":
    st.header("📖 Read a File")
    show_file_tree()
    st.divider()
    file_name = st.text_input("Enter file name to read")
    if st.button("Read File", type="primary"):
        if not file_name:
            st.warning("Please enter a file name.")
        else:
            p = Path(file_name)
            if p.exists():
                with open(file_name, 'r') as f:
                    data = f.read()
                st.subheader(f"📄 Contents of `{file_name}`")
                st.code(data, language="text")
            else:
                st.error("❌ FILE NOT FOUND!")

# ── Update File ───────────────────────────────────────────────────────────────
elif operation == "✏️ Update File":
    st.header("✏️ Update a File")
    show_file_tree()
    st.divider()
    file_name  = st.text_input("Enter file name to update")
    update_mode = st.radio("Update mode", ["Overwrite content", "Append content"])
    new_content = st.text_area("Enter new content")
    if st.button("Update File", type="primary"):
        if not file_name:
            st.warning("Please enter a file name.")
        else:
            p = Path(file_name)
            if p.exists():
                mode = 'w' if update_mode == "Overwrite content" else 'a'
                with open(file_name, mode) as f:
                    f.write(new_content)
                st.success(f"✅ File **{file_name}** updated successfully!")
            else:
                st.error("❌ FILE DOES NOT EXIST!")

# ── Delete File ───────────────────────────────────────────────────────────────
elif operation == "🗑️ Delete File":
    st.header("🗑️ Delete a File")
    show_file_tree()
    st.divider()
    file_name = st.text_input("Enter file name to delete")
    if st.button("Delete File", type="primary"):
        if not file_name:
            st.warning("Please enter a file name.")
        else:
            p = Path(file_name)
            if p.exists():
                os.remove(p)
                st.success(f"✅ File **{file_name}** deleted successfully!")
                st.rerun()
            else:
                st.error("❌ FILE DOES NOT EXIST!")

# ── Rename File ───────────────────────────────────────────────────────────────
elif operation == "🔤 Rename File":
    st.header("🔤 Rename a File")
    show_file_tree()
    st.divider()
    file_name     = st.text_input("Enter current file name")
    new_file_name = st.text_input("Enter new file name")
    if st.button("Rename File", type="primary"):
        if not file_name or not new_file_name:
            st.warning("Please fill in both fields.")
        else:
            p = Path(file_name)
            if p.exists():
                p.rename(new_file_name)
                st.success(f"✅ Renamed **{file_name}** → **{new_file_name}**!")
                st.rerun()
            else:
                st.error("❌ FILE NOT FOUND!")

# ── Create Folder ─────────────────────────────────────────────────────────────
elif operation == "📁 Create Folder":
    st.header("📁 Create a New Folder")
    show_file_tree()
    st.divider()
    folder_name = st.text_input("Enter folder name")
    if st.button("Create Folder", type="primary"):
        if not folder_name:
            st.warning("Please enter a folder name.")
        else:
            p = Path(folder_name)
            if p.exists():
                st.error("⚠️ FOLDER ALREADY EXISTS!")
            else:
                p.mkdir()
                st.success(f"✅ Folder **{folder_name}** created successfully!")
                st.rerun()

# ── Delete Folder ─────────────────────────────────────────────────────────────
elif operation == "❌ Delete Folder":
    st.header("❌ Delete a Folder")
    show_file_tree()
    st.divider()
    folder_name = st.text_input("Enter folder name to delete")
    if st.button("Delete Folder", type="primary"):
        if not folder_name:
            st.warning("Please enter a folder name.")
        else:
            p = Path(folder_name)
            if p.exists():
                try:
                    p.rmdir()
                    st.success(f"✅ Folder **{folder_name}** deleted successfully!")
                    st.rerun()
                except OSError:
                    st.error("⚠️ Folder is not empty. Remove its contents first.")
            else:
                st.error("❌ FOLDER NOT FOUND!")