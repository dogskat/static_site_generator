from textnode import TextType, TextNode


def main():
    my_textnode = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(my_textnode)

    other_textnode = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(f"otherand and  my the same?: {my_textnode == other_textnode}")

    diff_textnode = TextNode("This is a different text node", TextType.ITALIC, "https://www.boot.dev")
    print(f"diff and my the same?: {my_textnode == diff_textnode}")


if __name__ == "__main__":
    main()
