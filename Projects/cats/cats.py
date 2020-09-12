"""Typing test implementation"""

from utils import *
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    """
    li = []
    for p in paragraphs:
        if select(p):
            li += [p]
    if k < len(li):
        return li[k]
    else:
        return ''


def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    def select(paragraphs):
        formatted_paragraphs = split(remove_punctuation(lower(paragraphs)))
        for word in topic:
            if word in formatted_paragraphs:
                return True
        return False
    return select
 

def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    """
    typed_words = split(typed)
    reference_words = split(reference)

    total_accuracy = 100.0
    if typed_words:
        accuracy_decrement = 100/len(typed_words)
    else:
        return 0.0
    for i in range(len(typed_words)):
        if i > len(reference_words) - 1:
            total_accuracy -= accuracy_decrement * (len(typed_words) - i)
            return total_accuracy
        elif typed_words[i] != reference_words[i]:
            total_accuracy -= accuracy_decrement
    return total_accuracy


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'
    return len(typed)/5 * 60 / elapsed


def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than LIMIT.
    """
    valid_word = min(valid_words, key=lambda x: diff_function(user_word, x, limit))
    diff = diff_function(user_word, valid_word, limit)
    if diff > limit or user_word in valid_words:
        return user_word
    else:
        return valid_word


def shifty_shifts(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """
    if limit < 0:
        return 0
    elif len(start) == 0:
        return 0
    elif len(goal) > len(start):
        diff = len(goal) - len(start)
        return diff + shifty_shifts(start, goal[:-diff], limit - diff)
    elif len(start) > len(goal):
        diff = len(start) - len(goal)
        return diff + shifty_shifts(start[:-diff], goal, limit - diff)
    elif start[0] == goal[0]:
        return shifty_shifts(start[1:], goal[1:], limit)
    else:
        return 1 + shifty_shifts(start[1:], goal[1:], limit - 1)


def meowstake_matches(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL."""
    if limit < 0: 
        return 0
    elif not start or not goal:
        return abs(len(start) - len(goal))
    elif start[0] == goal[0]:
        return meowstake_matches(start[1:], goal[1:], limit)
    else:
        add_diff = meowstake_matches(goal[0] + start, goal, limit - 1) + 1
        remove_diff = meowstake_matches(start[1:], goal, limit - 1) + 1
        substitute_diff = meowstake_matches(goal[0] + start[1:], goal, limit - 1) + 1
        return min(add_diff, remove_diff, substitute_diff)


def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function'


###########
# Phase 3 #
###########


def report_progress(typed, prompt, id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    i = 0
    while i < len(typed) and typed[i] == prompt[i]:
        i += 1
    progress = i / len(prompt)
    send({'id': id, 'progress': progress})
    return progress


def fastest_words_report(times_per_player, words):
    """Return a text description of the fastest words typed by each player."""
    game = time_per_word(times_per_player, words)
    fastest = fastest_words(game)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def time_per_word(times_per_player, words):
    """Given timing data, return a game data abstraction, which contains a list
    of words and the amount of time each player took to type each word.

    Arguments:
        times_per_player: A list of lists of timestamps including the time
                          the player started typing, followed by the time
                          the player finished typing each word.
        words: a list of words, in the order they are typed.
    """
    times = []
    for i in range(len(times_per_player)):
        times.append([])
        for j in range(len(times_per_player[i]) - 1):
            times[i].append(times_per_player[i][j+1] - times_per_player[i][j])
    return game(words, times)


def fastest_words(game):
    """Return a list of lists of which words each player typed fastest.

    Arguments:
        game: a game data abstraction as returned by time_per_word.
    Returns:
        a list of lists containing which words each player typed fastest
    """
    players = range(len(all_times(game)))  # An index for each player
    words = range(len(all_words(game)))    # An index for each word
    lst = [[] for player in players]
    for word_index in words:
        best_player = 0
        best_time = time(game, best_player, word_index)
        for player_num in players:
            if time(game, player_num, word_index) < best_time:
                best_player = player_num
                best_time = time(game, player_num, word_index)
        lst[best_player].append(word_at(game, word_index))
    return lst


def game(words, times):
    """A data abstraction containing all words typed and their times."""
    assert all([type(w) == str for w in words]), 'words should be a list of strings'
    assert all([type(t) == list for t in times]), 'times should be a list of lists'
    assert all([isinstance(i, (int, float)) for t in times for i in t]), 'times lists should contain numbers'
    assert all([len(t) == len(words) for t in times]), 'There should be one word per time.'
    return [words, times]


def word_at(game, word_index):
    """A selector function that gets the word with index word_index"""
    assert 0 <= word_index < len(game[0]), "word_index out of range of words"
    return game[0][word_index]


def all_words(game):
    """A selector function for all the words in the game"""
    return game[0]


def all_times(game):
    """A selector function for all typing times for all players"""
    return game[1]


def time(game, player_num, word_index):
    """A selector function for the time it took player_num to type the word at word_index"""
    assert word_index < len(game[0]), "word_index out of range of words"
    assert player_num < len(game[1]), "player_num out of range of players"
    return game[1][player_num][word_index]


def game_string(game):
    """A helper function that takes in a game object and returns a string representation of it"""
    return "game(%s, %s)" % (game[0], game[1])

enable_multiplayer = True  # Change to True when you

##########################
# Extra Credit #
##########################

key_distance = get_key_distances()
def key_distance_diff(start, goal, limit):
    """ A diff function that takes into account the distances between keys when
    computing the difference score."""

    start = start.lower() #converts the string to lowercase
    goal = goal.lower() #converts the string to lowercase

    if limit < 0: 
        return float('inf')
    elif not start or not goal:
        return abs(len(start) - len(goal))
    elif start[0] == goal[0]:
        return key_distance_diff(start[1:], goal[1:], limit)
    else:
        key_score = key_distance[(start[0], goal[0])]
        add_diff = key_distance_diff(goal[0] + start, goal, limit - 1) + 1
        remove_diff = key_distance_diff(start[1:], goal, limit - 1) + 1
        substitute_diff = key_distance_diff(goal[0] + start[1:], goal, limit - key_score) + key_score
        return min(add_diff, remove_diff, substitute_diff)


def memo(f):
    """A memoization function as seen in John Denero's lecture on Growth"""

    cache = {}
    def memoized(*args):
        if args not in cache:
            cache[args] = f(*args)
        return cache[args]
    return memoized


key_distance_diff = memo(key_distance_diff)
key_distance_diff = count(key_distance_diff)
def faster_autocorrect(user_word, valid_words, diff_function, limit):
    """A memoized version of the autocorrect function implemented above."""
    valid_word = min(valid_words, key=lambda x: diff_function(user_word, x, limit))
    diff = diff_function(user_word, valid_word, limit)
    if diff > limit or user_word in valid_words:
        return user_word
    else:
        return valid_word


##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)
