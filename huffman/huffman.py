from __future__ import annotations
from argparse import ArgumentParser
from logging import error
from sys import exit
from math import ceil
import pygame


class Node:
    left: Node = None
    right: Node = None
    value: int = 0
    character: str = chr(0)

    def __init__(self, value: int, character: str = chr(0)) -> Node:
        self.value = value
        self.character = character

    def __str__(self) -> str:
        return f"{self.character or 'None'}: {self.value}"

    def __eq__(self, __o: object) -> bool:
        if type(__o) != Node:
            return False
        return self.character == __o.character and self.value == __o.value
    
    def __hash__(self) -> int:
        return ord(self.character) * 31 + self.value

    def count(self) -> int:
        result = 1
        if self.left is not None:
            result += self.left.count()
        if self.right is not None:
            result += self.right.count()
        return result
    
    def flatten(self) -> list:
        return [self] + (self.left.flatten() + self.right.flatten() if self.character is chr(0) else [])
    
    def traverse(self, path: str = "") -> dict:
        character_codes = {}
        if self.character is chr(0):
            path_l = path_r = path

            path_l += '0'
            path_r += '1'
            character_codes |= self.left.traverse(path_l) | self.right.traverse(path_r)
        else:
            character_codes[self.character] = path
        return character_codes
    
    def rebuild_tree(flat_rep: bytes) -> Node:
        root = Node(0, chr(flat_rep[0]))
        index = 1
        stack = [root]

        for index in range(1, len(flat_rep)):
            node = Node(0, chr(flat_rep[index]))
            parent = stack[-1]
            if parent.left is None:
                parent.left = node
            else:
                while parent.right is not None:
                    parent = stack.pop()
                parent.right = node
            if node.character == '\x00':
                stack.append(node)

        return root


def split_into_bytes(num: int) -> bytes:
    if num < 0:
        raise ValueError()
    if num == 0:
        return bytes([0])

    result = []
    for _ in range(ceil(num.bit_length) / 8):
        result.append(num & 0xff)
        num = num >> 8
    return bytes(result)

        

parser = ArgumentParser("Huffman En/Decoder", description="Encodes and decodes huffman encoded text files")
parser.add_argument("mode", choices=["encode", "decode"], help="Determines wether the input is treated as huffman encoded text or plain text")
parser.add_argument("-input", help="Input file for decoding/encoding. Leave empty to use the standard input")
parser.add_argument("-output", help="Output file for decoding/encoding. Leave empty to use the standard output")

parsed_args = parser.parse_args()

if parsed_args.input is None and parsed_args.mode == "decode":
    error("Cannot use standard input decoding huffman text!")
    exit(-1)

if parsed_args.output is None and parsed_args.mode == "encode":
    error("Cannot use standard output for encoding huffman text!")
    exit(-1)


eof_node = Node(1, chr(0x03))
nodes = {}

if parsed_args.mode == "encode":
    if parsed_args.input is None:
        text_input = "Lorem ipsum dolor sit amet" #input("Please enter the text you wish to encode\n")
    else:
        with open(parsed_args.input) as fh:
            text_input = fh.read()
    for char in text_input:
        if char in nodes:
            nodes[char].value += 1
        else:
            nodes[char] = Node(1, char)
    nodes = list(nodes.values())
    nodes.append(eof_node)
    nodes.sort(key=lambda elem: elem.value, reverse=True)

    while len(nodes) > 1:
        node1 = nodes.pop()
        node2 = nodes.pop()
        tree = Node(node1.value + node2.value)
        tree.left = node1
        tree.right = node2
        index = 0

        for sub_tree in nodes:
            if sub_tree.value > tree.value:
                index += 1

        nodes.insert(index, tree)

    tree = nodes.pop()
    count = tree.count()
    codes = tree.traverse()
    print(codes)

    with open(parsed_args.output, "w+b") as fh_out:
        fh_out.write(bytes([count&0xff00, count&0xff]))
        print(fh_out.write(bytes(map(lambda x: ord(x.character), tree.flatten()))))
        byte = 0
        bits = 0
        encoded_text = []
        for char in text_input + "\x03":
            code_list = codes[char]
            for dir in code_list:
                byte >>= 1
                byte += int(dir) * 0x80
                bits += 1
                if bits == 8:
                    encoded_text.append(byte)
                    byte = bits = 0
        
        if bits < 8:
            encoded_text.append(byte >> (8 - bits))

        fh_out.write(bytes(encoded_text))
elif parsed_args.mode == "decode":
    with open(parsed_args.input, mode="rb") as fh_in:
        length = int.from_bytes(fh_in.read(2), byteorder="big")
        print(length)
        tree = Node.rebuild_tree(fh_in.read(length))
        codes = dict((v, k) for k,v in tree.traverse().items())

        continue_reading = True
        decoded = ""
        code = ""

        for byte in fh_in.read():
            for _ in range(8):
                code += str((byte & 1))
                byte >>= 1
                if code in codes:
                    if codes[code] == chr(3):
                        continue_reading = False
                        break
                    else:
                        decoded += codes[code]
                        code = ""
        
        if parsed_args.output is None:
            print(decoded)
        else:
            with open(parsed_args.output, "wt+", encoding="utf-8") as fh_out:
                fh_out.write(decoded)
                fh_out.flush()


pygame.init()
pygame.font.init()

pygame.key.set_repeat(1000, 100)

"""def advance_tree_build():
    page = 0
    node1 = nodes.pop()
    node2 = nodes.pop()
    tree = Node(node1.value + node2.value)
    tree.left = node1
    tree.right = node2
    index = 0

    if len(nodes) > 2:
        while nodes[index].value > tree.value:
            index += 1
    nodes.insert(index, tree)
    

def render():
    global screen
    screen.fill(pygame.Color(240, 240, 240))
    screen.blit(font.render(f"{page+1}/{len(nodes)}", True, pygame.Color(0, 0, 0)), (0, 0))

    draw_tree(nodes[page])
    
    pygame.display.update()


def draw_tree(tree: Node, x_pos = 500, y_pos = 100, height = 1) -> None:
    pygame.draw.circle(screen, (0, 0, 0), (x_pos, y_pos), 12, 2)
    char = font.render(f"{tree.character}", False, (0, 0, 0))
    value = font.render(f"{tree.value}", False, (0, 0, 0))
    screen.blit(char, (x_pos-char.get_width()/2, y_pos-char.get_height()/2))
    screen.blit(value, (x_pos-value.get_width()/2, y_pos-value.get_height()/2-20))

    if tree.left is not None:
        new_x = x_pos - 500 / 2**height
        new_y = y_pos + 100
        pygame.draw.line(screen, (200, 0, 0), (x_pos-10, y_pos+10), (new_x+10, new_y-10))
        draw_tree(tree.left, new_x, new_y, height+1)
    
    if tree.right is not None:
        new_x = x_pos + 500 / 2**height
        new_y = y_pos + 100
        pygame.draw.line(screen, (200, 0, 0), (x_pos+10, y_pos+10), (new_x-10, new_y-10))
        draw_tree(tree.right, new_x, new_y, height+1)


def main():
    global page
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    advance_tree_build()
                if event.key == pygame.K_LEFT:
                    page = (page-1) % len(nodes)
                if event.key == pygame.K_RIGHT:
                    page = (page+1) % len(nodes)

        render()
            

if __name__ == "__main__":
    screen = pygame.display.set_mode((1000, 1000))
    font = pygame.font.Font(None, 24)
    page = 0

    main()"""
