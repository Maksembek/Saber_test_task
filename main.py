class ListNode:
    def __init__(self, data=None, prev=None, next=None, rand=None):
        self.data = data
        self.prev = prev
        self.next = next
        self.rand = rand


class ListRand:
    def __init__(self, head=None, tail=None, count=0):
        self.head = head
        self.tail = tail
        self.count = count

    def serialize(self, f):
        node_dict = {}
        node = self.head
        node_index = 0

        while node:
            node_dict[node] = node_index
            node_index += 1
            node = node.next

        node = self.head
        while node:
            f.write(str(len(node.data.encode("utf-8"))).encode("utf-8"))
            f.write(b' ')
            f.write(node.data.encode("utf-8"))
            f.write(b' ')
            if node.rand:
                f.write(str(node_dict[node.rand]).encode("utf-8"))
            else:
                f.write(b'-1')
            f.write(b' ')
            node = node.next

    def deserialize(self, f):
        node_data = f.read().split()
        node_index = 0
        self.head = self.tail = None
        nodes = []
        while node_index < len(node_data)-4:
            data_length = int(node_data[node_index])
            node_index += 1
            # node_string = "".join(node_data[node_index + 1:node_index + data_length + 1])
            node_string = "".join([x.decode() for x in node_data[node_index + 1:node_index + data_length + 1]])
            node_index += data_length + 1
            rand_index = int(node_data[node_index])
            node_index += 1
            node = ListNode(node_string, None, None, None)
            nodes.append(node)
            if self.head is None:
                self.head = self.tail = node
            else:
                node.prev = self.tail
                self.tail.next = node
                self.tail = node
            if rand_index != -1 and rand_index < len(nodes):
                node.rand = nodes[rand_index]
            self.count += 1


if __name__ == "__main__":
    # Create a linked list
    node1 = ListNode("Node I")
    node2 = ListNode("Node II")
    node3 = ListNode("Node III")
    node1.next = node2
    node2.next = node3
    node1.rand = node3
    node2.rand = node1

    linked_list = ListRand(node1, node3, 3)

    # Serialize the linked list to a file
    with open("linked_list.txt", "wb") as f:
        linked_list.serialize(f)

    # Deserialize the linked list from a file
    with open("linked_list.txt", "rb") as f:
        deserialized_linked_list = ListRand()
        deserialized_linked_list.deserialize(f)

    with open("linked_list_D.txt", "wb") as f:
        linked_list.serialize(f)

    with open("linked_list.txt", 'r') as f1, open("linked_list_D.txt", 'r') as f2:
        contents1 = f1.read()
        contents2 = f2.read()
        if contents1 == contents2:
            print("Files are the same")
        else:
            print("Files are different")
