import fire

from hello import hello


def main():
    print(hello())


if __name__ == "__main__":
    fire.Fire(main)
