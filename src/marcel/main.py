import readline

from marcel.osh import Command
from marcel.osh import KillCommandException
from marcel.osh.parse import Parser


def run_command(line):
    if line:
        try:
            pipeline = Parser(line).parse()
            command = Command(pipeline)
            command.execute()
        except KillCommandException as e:
            print(e, file=sys.stderr)


def process_input(handle_line):
    readline.parse_and_bind('set editing-mode emacs')
    try:
        while True:
            try:
                line = input(marcel.osh.env.ENV.prompt())
                handle_line(line)
            except KeyboardInterrupt:  # ctrl-C
                print()
    except EOFError:  # ctrl-D
        print()


def args():
    config_path = sys.argv[1] if len(sys.argv) > 1 else None
    return config_path


def main():
    config_path = args()
    marcel.osh.env.Environment.initialize(config_path)
    process_input(run_command)


if __name__ == '__main__':
    main()