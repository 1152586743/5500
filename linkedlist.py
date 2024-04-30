import streamlit as st
from graphviz import Digraph, nohtml

st.header("LinkedList Visualizer")
st.markdown("Enter a **value** on the left and click **add** to start your LinkedList! Number in the bracket after the value is corresponding index.")

viz_elt = st.empty()

with st.sidebar.form("ll_entry"):
    st.header("Enter a value to add:")
    user_val = st.text_input("Value")
    submitted = st.form_submit_button("Click to add")

#@title define-ll-and-visualizer

### Regular (non-circular) LinkedList definition:

class LinkedList:
  def __init__(self):
    self.root = None

  def append(self, item: object) -> None:
    if self.root is None:
      self.root = LLNode(item)
    else:
      self.root.append(item)

  def insert(self, item: object, index: int) -> None:
      if index == 0:
          new_node = LLNode(item)
          new_node.next = self.root
          self.root = new_node
      else:
          prev = None
          current = self.root
          current_index = 0
          while current_index < index and current is not None:
              prev = current
              current = current.next
              current_index += 1
          if prev is not None:
              new_node = LLNode(item)
              new_node.next = current
              prev.next = new_node

  def delete(self, index: int) -> None:
      if index == 0:
          self.root = self.root.next
      else:
          prev = None
          current = self.root
          current_index = 0
          while current_index < index and current is not None:
              prev = current
              current = current.next
              current_index += 1
          if prev is not None:
              prev.next = current.next

  def retrieve(self, index: int) -> object:
      current = self.root
      current_index = 0
      while current_index < index and current is not None:
          current = current.next
          current_index += 1
      if current is not None:
          return current.content
  def sort(self):
      if self.root is None or self.root.next is None:
          return
      # Bubble sort 
      changed = True
      while changed:
          current = self.root
          prev = None
          changed = False
          while current is not None and current.next is not None:
              if current.content > current.next.content:
                  changed = True
                  if prev is None:
                      tmp = current.next
                      current.next = tmp.next
                      tmp.next = current
                      self.root = tmp
                      prev = tmp
                  else:
                      tmp = current.next
                      current.next = tmp.next
                      tmp.next = current
                      prev.next = tmp
                      prev = tmp
              else:
                  prev = current
                  current = current.next      
        
  def __len__(self) -> int:
    if self.root is None:
      return 0
    else:
      return len(self.root)

  def to_string(self) -> str:
    if self.root is None:
      return 'LinkedList[]'
    else:
      return f'LinkedList[{self.root.to_string()}]'

  def __str__(self) -> str:
    return self.to_string()

  def __repr__(self) -> str:
    return self.to_string()

class LLNode:
  def __init__(self, item: object):
    self.content = item
    self.next = None

  def append(self, item: object) -> None:
    if self.next is None:
      self.next = LLNode(item)
    else:
      self.next.append(item)

  def __len__(self) -> int:
    if self.next is None:
      return 1
    else:
      return 1 + len(self.next)

  def to_string(self) -> str:
    content_str = f'LLNode[{self.content}] '
    if self.next is None:
      return content_str
    else:
      next_str = self.next.to_string()
      return f'{content_str}{next_str}'

  def __str__(self) -> str:
    return self.to_string()

  def __repr__(self) -> str:
    return self.to_string()

# Helper function for visualizing both regular and circular linked lists:

def visualize_ll(ll):
    dot = Digraph(
        graph_attr={'rankdir': 'LR'},
        node_attr={'shape': 'record', 'height': '.1'}
    )
    node_pointer = ll.root
    index = 0
    prev_node_name = None

    while node_pointer is not None:
        node_label = f'{node_pointer.content} ({index})'  # Include index in the label
        node_name = f'node{index}'  # Create a unique node name using the index
        
        # Create node with label
        dot.node(name=node_name, label=nohtml('<f0> |' + node_label + '|<f1>'))

        # Connect the current node with the previous node if not the first node
        if prev_node_name is not None:
            dot.edge(f'{prev_node_name}:f1', f'{node_name}:f0')

        # Update previous node name and move to the next node
        prev_node_name = node_name
        node_pointer = node_pointer.next
        index += 1

    viz_elt.graphviz_chart(dot)


if 'palette' not in st.session_state:
    st.session_state['palette'] = LinkedList()

visualize_ll(st.session_state['palette'])

if submitted:
    if user_val == "":
      st.sidebar.error("Please enter a value")
    else:
      st.session_state['palette'].append(user_val)
      st.toast(f"Added {user_val}")
      
with st.sidebar:
    st.header("Operations")
    # inserting items
    add_val = st.text_input("Value to insert")
    add_index = st.number_input("Index to insert at", min_value=0, format="%d")
    add_btn = st.button("insert")

    # Deleting items
    del_index = st.number_input("Index to delete at", min_value=0, format="%d")
    del_btn = st.button("Delete")

    # Retrieving items
    get_index = st.number_input("Index to get value from", min_value=0, format="%d")
    get_btn = st.button("Get Value")

    # Sorting
    sort_btn = st.button("Sort List From Low to High")

if add_btn:
    if add_index is None or add_index == 0:
        st.session_state['palette'].append(add_val)
    else:
        st.session_state['palette'].insert(add_val, add_index)
    st.toast(f"Added {add_val} at index {add_index}")
    visualize_ll(st.session_state['palette'])

if del_btn:
    st.session_state['palette'].delete(del_index)
    st.toast(f"Deleted item at index {del_index}")
    visualize_ll(st.session_state['palette'])

if get_btn:
    value = st.session_state['palette'].retrieve(get_index)
    if value is not None:
        st.sidebar.write(f"Value at index {get_index}: {value}")
    else:
        st.sidebar.error("No value found at that index.")
    visualize_ll(st.session_state['palette'])

if sort_btn:
    st.session_state['palette'].sort()
    st.toast("List sorted")
    visualize_ll(st.session_state['palette'])


visualize_ll(st.session_state['palette'])
