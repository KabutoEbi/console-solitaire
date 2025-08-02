from game import Game

def main():
    game = Game()

    while True:
        print("\n" + "="*40)
        game.print_state()
        print("="*40)
        if game.is_win():
            print("\nCongratulations! Game Clear!")
            again = input("Start a new game? (y/n): ").strip().lower()
            if again == 'y':
                game = Game()
                continue
            else:
                break
        print(f"\nScore: {game.get_score()}  Moves: {game.get_moves()}")
        print("-"*40)
        print("Command: d(draw) m(move tableau) f(to foundation) b(to tableau) r(reset) u(undo) t(stuck) q(quit)")
        print("-"*40)
        cmd = input("Input Command: ").strip().lower()
        if cmd == 'd':
            game.draw_from_stock()
        elif cmd == 'm':
            try:
                src = int(input("Source tableau column (1-7): ")) - 1
                dst = int(input("Destination tableau column (1-7): ")) - 1
                count = int(input("Number of cards to move (>=1): "))
                game.move_tableau_to_tableau(src, dst, count)
            except Exception as e:
                print(f"Input Error: {e}")
        elif cmd == 'f':
            try:
                src_type = input("Source (t: tableau, w: waste): ").strip().lower()
                if src_type == 't':
                    idx = int(input("Tableau column (1-7): ")) - 1
                    game.move_to_foundation('t', idx)
                elif src_type == 'w':
                    game.move_to_foundation('w')
                else:
                    print("Input t or w")
            except Exception as e:
                print(f"Input Error: {e}")
        elif cmd == 'w':
            try:
                dst = int(input("Destination tableau column (1-7): ")) - 1
                game.move_waste_to_tableau(dst)
            except Exception as e:
                print(f"Input Error: {e}")
        elif cmd == 'b':
            try:
                src_type = input("Source (t: foundation, w: waste): ").strip().lower()
                if src_type == 't':
                    foundation_idx = int(input("Foundation number (1-4): ")) - 1
                    tableau_idx = int(input("Destination tableau column (1-7): ")) - 1
                    game.move_foundation_to_tableau(foundation_idx, tableau_idx)
                elif src_type == 'w':
                    tableau_idx = int(input("Destination tableau column (1-7): ")) - 1
                    game.move_waste_to_tableau(tableau_idx)
                else:
                    print("Input t or w")
            except Exception as e:
                print(f"Input Error: {e}")
        elif cmd == 'r':
            print("Resetting game. Starting new game.")
            game = Game()
        elif cmd == 'q':
            print("Exiting game.")
            break
        elif cmd == 'u':
            game.undo()
        elif cmd == 't':
            if game.is_stuck():
                print("No more valid moves (stuck).")
            else:
                print("There are still valid moves.")
        else:
            print("Unknown command. Please input d, m, f, w, b, r, u, t, h, or q.")

if __name__ == "__main__":
    main()
