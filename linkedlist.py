import streamlit as st
from graphviz import Digraph, nohtml

st.header("LinkedList Visualizer")
st.markdown("Enter a **value** on the left and click **Submit** to update the visualization!")

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
  visited_nodes = []
  prev_node_name = None
  node_pointer = ll.root
  while node_pointer is not None:
    # New node
    cur_name = str(node_pointer.content)
    if cur_name in visited_nodes:
      break
    dot.node(name=cur_name, label=nohtml('{<f0> '+cur_name+'|<f1>}'))
    # And edge from prev to cur, if not None
    if prev_node_name is not None:
      edge_from = f'{prev_node_name}:f1'
      dot.edge(edge_from, cur_name)
    # Now we can update prev_node_name
    visited_nodes.append(cur_name)
    prev_node_name = cur_name
    node_pointer = node_pointer.next
  viz_elt.graphviz_chart(dot)

if 'palette' not in st.session_state:
  st.session_state['palette'] = LinkedList()
  st.session_state['palette'].append('red')
  st.session_state['palette'].append('green')
  st.session_state['palette'].append('blue')

visualize_ll(st.session_state['palette'])
if submitted:
    if user_val == "":
      st.sidebar.error("Please enter a value")
    else:
      st.session_state['palette'].append(user_val)
      st.toast(f"Added {user_val}")
    visualize_ll(st.session_state['palette'])
