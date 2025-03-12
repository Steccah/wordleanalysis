from random import randint


def analyze_letter_positions(filename):
    # Initialize dictionaries for each position
    position_frequencies = [{} for _ in range(5)]
    total_words = 0

    # Read the file
    with open(filename, 'r') as file:
        for line in file:
            word = line.strip().lower()
            if len(word) == 5:  # Ensure word is 5 letters
                total_words += 1
                for pos, letter in enumerate(word):
                    position_frequencies[pos][letter] = position_frequencies[pos].get(letter, 0) + 1

    # Print results for each position
    for pos, freq_dict in enumerate(position_frequencies):
        # print(f"\nPosition {pos + 1} most common letters:")
        # Sort by frequency and get top 10
        sorted_letters = sorted(freq_dict.items(), key=lambda x: x[1], reverse=True)[:10]
        for letter, count in sorted_letters:
            percentage = (count / total_words) * 100
            # print(f"{letter}: {count} times ({percentage:.1f}%)")
    
    return position_frequencies, total_words

def rank_words_by_letter_position_by_filename(filename, position_frequencies, total_words, top_n=100):
    dictionary = []
    with open(filename, 'r') as file:
        for line in file:
            dictionary.append(line)

    return rank_words_by_letter_position(dictionary, position_frequencies, total_words, top_n)
            

def rank_words_by_letter_position(dictionary, position_frequencies, total_words, top_n=100):
    word_scores = {}

    for word in dictionary:
        word = word.strip().lower()
        score = 0
        for pos, letter in enumerate(word):
            # Score based on letter frequency at this position
            letter_count = position_frequencies[pos].get(letter, 0)
            score += letter_count / total_words

        if duplicate_letters(word):
            score -= 0.3
            
        word_scores[word] = score

    # Sort words by score
    ranked_words = sorted(word_scores.items(), key=lambda x: x[1], reverse=True)

    return ranked_words

def duplicate_letters(word):
    for letter in word:
        if word.count(letter) > 1:
            return True
    return False

def filter_words_by_banned_letters(words, banned_letters):
    filtered_words = []
    for word in words:
        for pos in range(5):
            if word[pos] in banned_letters[pos]:
                break
        else:
            filtered_words.append(word)
    return filtered_words

def filter_words_by_mandatory_letters(words, mandatory_letters):
    filtered_words = []
    for word in words:
        add = True
        for pos in range(5):
            if mandatory_letters[pos] != "":
                if word[pos] == mandatory_letters[pos]:
                    pass
                    # filtered_words.append(word)
                else:
                    add = False
                    break
        if add:
            filtered_words.append(word)
    return filtered_words

def filter_words_by_yellow_letters(words, yellow_letters):
    filtered_words = []
    for word in words:
        add = True
        for l in yellow_letters:
            if l != "-":
                if l in word:
                    pass
                else:
                    add = False
                    break
        if add:
            filtered_words.append(word)
                
    return filtered_words

def guess():
    filename = "curated.txt"
    position_frequencies, total_words = analyze_letter_positions(filename)
    dictionary = rank_words_by_letter_position_by_filename("answers.txt", position_frequencies, total_words)

    dict = []
    for w in dictionary:
        dict.append(w[0])

    # print(dictionary[:100])

    banned_letters = [[], [], [], [], []]
    mandatory_letters = ["", "", "", "", ""]
    yellow_letters = ''
    count = 0

    while True:
        ranked = rank_words_by_letter_position(dict, position_frequencies, total_words, 10)
        print(f"Most probable word: {ranked[0][0]}")
        if len(ranked) == 1:
            return
        most_probable_word = ranked[0][0]
        bad = input(f"grey  : ")
        for l in bad:
            banned_letters[0].append(l)
            banned_letters[1].append(l)
            banned_letters[2].append(l)
            banned_letters[3].append(l)
            banned_letters[4].append(l)
        
        yellow = input(f"yellow: ")
        if yellow != '':
            yellow_letters += yellow
            for pos in range(5):
                if yellow[pos] != "-":
                    banned_letters[pos].append(yellow[pos])
        
        green = input(f"green : ")
        if green != "":
            for pos in range(5):
                if green[pos] != "-":
                    mandatory_letters[pos] = green[pos]

        for pos in range(5):
            if mandatory_letters[pos] != "":
                if mandatory_letters[pos] in banned_letters[pos]:
                    banned_letters[pos].remove(mandatory_letters[pos])

        if count == 1 or (green != "" and green.count("-") <= 2):
            dict = []
            with open("curatedunlimited.txt", "r") as file:
                for line in file:
                    dict.append(line.strip().lower())

        dict = filter_words_by_banned_letters(dict, banned_letters)
        dict = filter_words_by_mandatory_letters(dict, mandatory_letters)
        dict = filter_words_by_yellow_letters(dict, yellow_letters)
        count += 1

class Guesser :
    def __init__(self):
        self.filename = "curated.txt"
        self.position_frequencies, self.total_words = analyze_letter_positions(self.filename)
        self.dictionary = rank_words_by_letter_position_by_filename("curatedunlimited.txt", self.position_frequencies, self.total_words)

        self.dict = []
        for w in self.dictionary:
            self.dict.append(w[0])

        self.banned_letters = [[], [], [], [], []]
        self.mandatory_letters = ["", "", "", "", ""]
        self.yellow_letters = ''
        self.count = 0

    def guess(self, bad, yellow, green):
        ranked = rank_words_by_letter_position(self.dict, self.position_frequencies, self.total_words, 10)
        # print(f"Most probable word: {ranked[0][0]}")

        for l in bad:
            self.banned_letters[0].append(l)
            self.banned_letters[1].append(l)
            self.banned_letters[2].append(l)
            self.banned_letters[3].append(l)
            self.banned_letters[4].append(l)
        
        if yellow != '':
            self.yellow_letters += yellow
            for pos in range(5):
                if yellow[pos] != "-":
                    self.banned_letters[pos].append(yellow[pos])
        
        if green != "":
            for pos in range(5):
                if green[pos] != "-":
                    self.mandatory_letters[pos] = green[pos]

        for _ in range(5):
            for pos in range(5):
                if self.mandatory_letters[pos] != "":
                    if self.mandatory_letters[pos] in self.banned_letters[pos]:
                        self.banned_letters[pos].remove(self.mandatory_letters[pos])

        # self.dict = []
        # with open("curatedunlimited.txt", "r") as file:
        #     for line in file:
        #         self.dict.append(line.strip().lower())

        self.dict = filter_words_by_banned_letters(self.dict, self.banned_letters)
        self.dict = filter_words_by_mandatory_letters(self.dict, self.mandatory_letters)
        self.dict = filter_words_by_yellow_letters(self.dict, self.yellow_letters)
        self.count += 1
        ranked = rank_words_by_letter_position(self.dict, self.position_frequencies, self.total_words, 10)

        return ranked[0][0]

class Wordle:
    def __init__(self):
        self.count = 0
        self.get_sequential_word()
        print("word to gues: " + self.word)

    def get_random_word(self):
        with open("curatedunlimited.txt", "r") as file:
            words = file.readlines()

        random = randint(0, len(words))
        self.word = words[random].strip().lower()

    def get_sequential_word(self):
        with open("curatedunlimited.txt", "r") as file:
            words = file.readlines()

        self.word = words[self.count].strip().lower()
        # self.word = "globo"
        self.count += 1

    def guess(self, guess):
        # Initialize the output lists for each color
        green = ['-' for _ in range(5)]
        yellow = ['-' for _ in range(5)]
        bad = []  # We can collect bad letters separately

        # Create a letter frequency dictionary for the target word
        count = {}
        for letter in self.word:
            count[letter] = count.get(letter, 0) + 1

        # First pass: mark greens and update letter counts
        for i in range(5):
            if guess[i] == self.word[i]:
                green[i] = guess[i]
                count[guess[i]] -= 1

        # Second pass: mark yellows if the letter is in the word (with remaining count), otherwise mark as bad
        for i in range(5):
            if guess[i] != self.word[i]:
                if guess[i] in count and count[guess[i]] > 0:
                    yellow[i] = guess[i]
                    count[guess[i]] -= 1
                else:
                    bad.append(guess[i])

        # remove bad if they are in yellow
        for i in range(5):
            if yellow[i] != "-":
                if yellow[i] in bad:
                    bad.remove(yellow[i])
                    
        return ''.join(bad), ''.join(yellow), ''.join(green)

if __name__ == "__main__":

    counter = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

    wordle = Wordle()
    while True:

        guesser = Guesser()
        wordle.get_sequential_word()
        word = "sarto"
        bad, yellow, green = wordle.guess(word)
        count = 0

        while bad != "" and green != "" and yellow != "":
            count += 1
            bad, yellow, green = wordle.guess(word)
            print(bad, yellow, green)
            word = guesser.guess(bad, yellow, green)

        counter[count] = counter.get(count, 0) + 1
        print(counter)
        