import json
from pathlib import Path
import random
import argparse

parser = argparse.ArgumentParser(description="A spaced repetition program with import export and logging features")
parser.add_argument('--export_to', default=None)
parser.add_argument('--import_from', default=None)

args = parser.parse_args()
importt = args.import_from
exportt = args.export_to

log_file = []

def print_2(text):
    log_file.append(text)
    print(text)

def input_2(text):
    log_file.append(text)
    return input(text)
# add and exit function are working
class Menu:


    def __init__(self):
        self.deck = Deck()

    def ask(self):
        number = int(input_2('How many times to ask?'))
        print_2('How many times to ask?')
        self.deck.start(number)

    def add(self):
        self.deck.add_card(self)  # Working

    def remove(self):
        term_to_remove = input_2('Which card?\n')

        self.deck.remove_card(term_to_remove)  # Working

    def import_cards(self, file=None):
        if file == None:
            file_name = input_2('File name:\n')

            try:

                p = Path(file_name)
                if p.name.endswith('.json'):
                    pass
                else:
                    p.rename(p.with_suffix('.json'))
                file_name = file_name.split('.')[0] + '.json'
                with open(file_name, 'r') as file:
                    imported_deck = json.load(file)
                    for card in imported_deck:
                        term = list(card.keys())[0]
                        mistakes = card["mistake"]
                        definition = card[term]
                        self.deck.add_card(Card(term, definition, mistakes))
                    print_2(f'{len(imported_deck)} cards have been loaded.')
            except FileNotFoundError:
                print_2('File not found.')
            else:
                p = Path(file_name.split('.')[0] + '.json')
                p.rename(p.with_suffix('.txt'))
        else:
            try:

                p = Path(file)
                if p.name.endswith('.json'):
                    pass
                else:
                    p.rename(p.with_suffix('.json'))
                file_name = file.split('.')[0] + '.json'
                with open(file_name, 'r') as filee:
                    imported_deck = json.load(filee)
                    for card in imported_deck:
                        term = list(card.keys())[0]
                        mistakes = card["mistake"]
                        definition = card[term]
                        self.deck.add_card(Card(term, definition, mistakes))
                    print_2(f'{len(imported_deck)} cards have been loaded.')
            except FileNotFoundError:
                print_2('File not found.')
            else:
                p = Path(file.split('.')[0] + '.json')
                p.rename(p.with_suffix('.txt'))

    def export(self, file_name=None):

        if file_name == None:
            file_name = input_2('File name:\n').split('.')[0] + '.json'
            with open(file_name, 'w') as file:
                json.dump(self.deck.cards, file, default=lambda o: o.__dict__(), indent=4)
            p = Path(file_name)
            p.rename(p.with_suffix('.txt'))
            print_2(f'{len(self.deck)} cards have been saved.')
        elif (len(self.deck))==0:
            with open(file_name,'w') as file:
                print_2('0 cards have been saved.')

        else:
            with open(file_name, 'w') as file:
                json.dump(self.deck.cards, file, default=lambda o: o.__dict__(), indent=4)
            p = Path(file_name)
            p.rename(p.with_suffix('.txt'))
            print_2(f'{len(self.deck)} cards have been saved.')


    def log(self):
        file_name = input_2('File name:\n')
        with open(file_name, 'w') as f:
            for line in log_file:
                f.write(line)




        print_2('The log has been saved.\n')

    def hardest_card(self):
        cards_mistakes = [i.mistake for i in self.deck.cards]
        if all(cards_mistakes)==False or len(cards_mistakes)==0:
            print_2('There are no cards with errors.')
        elif cards_mistakes.count(max(cards_mistakes)) ==1:
            print_2(f'The hardest card is "{self.deck.cards[cards_mistakes.index(max(cards_mistakes))].term}". You have {max(cards_mistakes)} errors answering it.')
        else:
            statement = 'The hardest cards are '
            cards = [i for i in self.deck.cards if i.mistake == max(cards_mistakes)]
            for i in range(len(cards)-1):

                statement +=f'{cards[i].term},'
            statement += f' and {cards[-1].term}'
            print_2(statement)

    def reset_stats(self):
        for card in self.deck.cards:
            card.mistake = 0

        print_2('Card statistics have been reset.')


    def exit(self):
        print_2('Bye bye!')
        if exportt!=None:
            self.export(exportt)


        exit()

    def start(self):
        action = ''
        while action != 'exit':
            action = input_2('Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):\n').lower()
            if action == 'add':
                self.add()
            elif action == 'remove':
                self.remove()
            elif action == 'import':
                self.import_cards()
            elif action == 'export':
                self.export()
            elif action == 'ask':
                self.ask()
            elif action == 'log':
                self.log()
            elif action == 'hardest card':
                self.hardest_card()
            elif action == 'reset stats':
                self.reset_stats()
            elif action == 'exit':
                self.exit()


class Deck:
    def __init__(self):
        self.cards = []
        self.number_of_cards = len(self)

    def __len__(self):
        return len(self.cards)

    def __repr__(self):
        return str(self.cards)

    def remove_card(self, card_remove):
        for index in range(len(self)):
            if self.cards[index].term == card_remove:
                self.cards.pop(index)
                print_2(f'The card has been removed.\n')
                return True
        print_2(f'Can\'t remove "{card_remove}": there is no such card.')
        return False

    def add_card(self, card=None):
        if isinstance(card, Card):
            if self.term_exists(card.term) == True:
                return None
            if self.definition_exists(card.definition) == True:
                return None
            self.cards.append(card)
        else:
            term_string = f'The card:\n'
            def_string = f'The definition of the card:\n'
            while True:
                card_term = input_2(term_string)
                if self.term_exists(card_term) == False:
                    break
                term_string = f'The card "{card_term}" already exists. Try again:\n'

            while True:
                card_definition = input_2(def_string)
                if self.definition_exists(card_definition) == False:
                    break
                def_string = f'The definition "{card_definition}" already exists. Try again:\n'

            self.cards.append(Card(card_term, card_definition))
            print_2(f'The pair ("{card_term}":"{card_definition}") has been added.\n')

    def start(self, num):
        '''
        for i in range(self.number_of_cards):
            term_string = f'The term for card #{i + 1}\n'
            def_string = f'The definition for card #{i + 1}\n'
            while True:
                card_term = input_2(term_string)
                if self.term_exists(card_term)==False:
                    break
                term_string=''

            while True:
                card_definition = input_2(def_string)
                if self.definition_exists(card_definition)==False:
                    break
                def_string=''
            self.add_card(Card(card_term, card_definition))
        '''
        for i in range(num):
            card = random.choice(self.cards)
            card.test()
            if card.answer == False:
                card.mistake+=1
                sim_check = self.check_similair_answer(card.reponse)
                if sim_check != None:
                    print_2(
                        f'Wrong answer. The right answer is "{card.definition}", but your definition is correct for "{sim_check}".')
                else:
                    print_2(f'Wrong. The right answer is "{card.definition}".')

    def term_exists(self, term_to_check):
        # term_print_2 = f'The card "{term_to_check}" already exists. Try again:'
        terms = [card.term for card in self.cards]
        if term_to_check in terms:
            return True
        else:
            return False

    def definition_exists(self, definition_to_check):
        # definition_print_2 = f'The definition "{definition_to_check}" already exists. Try again.'
        definitions = [card.definition for card in self.cards]
        if definition_to_check in definitions:
            # print_2(definition_print_2)
            return True
        else:
            return False

    def check_similair_answer(self, answer):
        for card in self.cards:
            if card.definition == answer:
                return card.term
        return None


class Card():

    def __init__(self, term, definition, mistake=0):
        self.term = term
        self.definition = definition
        self.answer = None
        self.reponse = ''
        self.mistake = mistake

    def __dict__(self):
        return {self.term: self.definition,
                "mistake": self.mistake}

    def __str__(self):
        return f'("{self.term}":"{self.definition}")'

    def test(self):
        self.reponse = input_2(f'Print the definition of "{self.term}":\n')
        if self.reponse == self.definition:
            print_2('Correct!')
            self.answer = True
        else:
            # print_2(f'Wrong. The right answer is "{self.definition}".')
            self.answer = False

    def __repr__(self):
        return {'term': self.term, 'definition': self.definition}


# number = int(input_2_2('input_2 the number of cards:\n'))
# deck = Deck(number)
menu = Menu()
if importt!=None:
    menu.import_cards(importt)

menu.start()
