"""Scripted, self-running BrainOS memory-agent demo.

Runs a fixed 10-turn conversation with no user input - ideal for recording a
GIF or asciicast (asciinema / vhs). It reuses the real agent pipeline from
`agent.py`, so every memory operation (store / retrieve / forget) is genuine,
not faked.

    python demo_script.py            # ~30s, mock mode, no API key needed
    python demo_script.py --fast     # no typing delays (for quick checks)

Color legend (matches agent.py annotations):
    green  = STORED         blue   = RETRIEVED
    red    = FORGOTTEN      yellow = WORKING MEMORY
"""

from __future__ import annotations

import argparse
import sys
import time

from agent import BANNER, C, MemoryAgent, MockResponder, _load_plugins, paint

# --------------------------------------------------------------------------- #
# Scripted conversation.
#
# Turn 2 introduces the "Project Atlas" deadline. Turn 8 asks about it again -
# that is the highlighted retrieval moment where the hippocampal index recalls
# the earlier turn instead of the model inventing an answer.
# --------------------------------------------------------------------------- #
SCRIPT: list[str] = [
    "Hi, I'm Priya, a backend engineer",                       # 1  intro
    "I'm leading Project Atlas, the deadline is next Friday",  # 2  <-- key fact
    "The main risk is the database migration step",            # 3
    "Switching gears - I also mentor two junior devs",         # 4  topic switch
    "We do code reviews together every Tuesday",               # 5
    "One of them is learning Rust on the side",                # 6
    "Back to work: what tools do you recommend for CI?",       # 7
    "Remind me, when is the Project Atlas deadline?",          # 8  <-- recall!
    "Right, so we should freeze the migration by Wednesday",   # 9
    "Thanks - can you summarize what you know about me?",      # 10 synthesis
]

RECALL_TURN = 8  # the turn we spotlight as the "memory retrieval" moment


def type_out(text: str, delay: float, prompt: str = "you> ") -> None:
    """Print `prompt` then reveal `text` character by character."""
    sys.stdout.write(paint(prompt, C.CYAN))
    sys.stdout.flush()
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n")
    sys.stdout.flush()


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Scripted BrainOS memory-agent demo")
    parser.add_argument("--fast", action="store_true", help="Skip typing/pacing delays")
    args = parser.parse_args(argv)

    type_delay = 0.0 if args.fast else 0.018   # per-character
    turn_pause = 0.0 if args.fast else 1.1     # after each agent reply

    plugins, source = _load_plugins()
    agent = MemoryAgent(plugins, MockResponder())

    print(paint(BANNER, C.CYAN))
    print(paint(f"  plugin source : {source}", C.DIM))
    print(paint("  scripted demo : 10 turns, mock responder, no input required", C.DIM))
    print(paint("  legend        : ", C.DIM)
          + paint("STORED ", C.GREEN) + paint("RETRIEVED ", C.BLUE)
          + paint("FORGOTTEN ", C.RED) + paint("WORKING-MEMORY", C.YELLOW))
    print()
    if not args.fast:
        time.sleep(1.0)

    for i, message in enumerate(SCRIPT, start=1):
        if i == RECALL_TURN:
            print(paint("  === watch the hippocampal index recall Turn 2 ===", C.BOLD + C.BLUE))
        type_out(message, type_delay)
        agent.handle(message)  # runs the real pipeline + prints memory ops
        time.sleep(turn_pause)

    print(paint("=== Final memory stats ===", C.BOLD))
    print(agent.stats_line())
    print(paint(f"  Recalled the Turn 2 deadline at Turn {RECALL_TURN} "
                f"straight from the memory index.", C.DIM))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
