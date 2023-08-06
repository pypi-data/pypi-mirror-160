"""
Handles the Grammar of the document

Classes
-------
- DiceString
- Die
- Operator
    - LeftHandOperator
        - GreaterThan
        - Exploding

"""
import logging
import math
import random
import re

logger = logging.getLogger('snakeeyes.elements')


class Die():
    """
    Generates the dice string to put through the system

        Attributes
        ----------
        parsestring : Pattern
            Regex pattern to detect the various attributes of a dice roll

        quantity : int
            Number of times die must be rolled

        sides : int
            Number of sides a die has

    """
    sides = 0
    quantity = 0

    def __init__(self, quantity: int, sides: int, oplist: list, string: str):
        """
        Initialize the string.

        Args:
            self: (todo): The instance
            quantity: (int): Number of dice to be rolled
            sides: (int): String which contains the sides of each die. Should be castable to int.
        """
        logger.debug("Initating DiceString")
        try:
            self.quantity = quantity
            self.sides = sides
            self.ops = oplist
            self.string = string
            logger.debug("Sides: %i \n Quantity: %i ",
                         self.sides, self.quantity)
        except (ValueError, AttributeError):
            pass

class CombatDie(Die):
    sides = 6
    def __init__(self, quantity: int, string: str, value: int, sides=6, opslist=[]):
        Die.__init__(self, quantity, sides, opslist, string)
        self.value = value

class DiceGroup():
    """Class that handles dice rolls using regular expressions.

    Attributes
    ----------
    string : str
        String to be processed
    dice : list
        List of dice rolled.
    """
    parsestring = re.compile(
        r"(?P<quantity> \d* (?=d\d*)) d (?P<sides>\d*)(?:[x\>\<dlh]\d*)*", re.X)
    parseops = re.compile(
        r"(?P<operator>[x\>\<]|dl|dh) (?P<operands>\d*)", re.X)
    parsecombat = re.compile(
        r"(?P<quantity> \d* (?=c)) c (?P<value>\d*)", re.X)

    def __init__(self, string: str):
        """
        Initialize a group of dice from the string.

        Args:
            self: The Instance.
            string: (str): The string to be processed.
        """
        self.string = string
        logger.debug("String: %s", self.string)
        __dice = self.parsestring.finditer(string)
        __combat_dice = self.parsecombat.finditer(string)
        self.dice = []
        self.combatdice = []
        for d in __dice:
            # Intiialize the dice
            quant = int(d.group('quantity'))
            sides = int(d.group('sides'))
            dstring = d.group()
            ops = self.parseops.finditer(dstring)
            opslist = []
            for o in ops:
                # initialize operator tuples
                optuple = (o.group('operator'), int(o.group('operands')))
                opslist.append(optuple)
            dicestring = Die(quant, sides, opslist, dstring)
            self.dice.append(dicestring)

            logger.debug(f"Oplist: {opslist}")
        for c in __combat_dice:
            quant = int(c.group('quantity'))
            value = int(c.group('value'))
            cstring = c.group()
            cdicestring = CombatDie(quant, cstring, value)
            self.dice.append(cdicestring)

        logger.debug(f"Dice: {self.dice}")

    def __bool__(self):
        """
        Returns true if the dice is true false otherwise.

        Args:
            self:: The instance
        """
        if self.dice:
            logger.debug("Die is true")
            return True
        return False

class Result():
    is_successful = False
    is_exploded = False

    def __init__(self, value):
        self.value = value

class CombatResult(Result):
    is_blank = False
    is_crit = False

    def __init__(self, value, effect):
        self.value = 0
        match value:
            case 1:
                self.value = 1
            case 2:
                self.value = 2
            case 3:
                self.value = 0
                self.is_blank = True
            case 4:
                self.value = 0
                self.is_blank = True
            case 5: 
                self.value = 0
                self.is_blank = True
            case 6:
                self.value = effect
                self.is_crit = True
        logger.debug(f"Combat Dice value: {self.value}")
            

class RollResult():
    """Results of an operation
    """

    def __init__(self, rolls: Result, total: int, dice_string: str, die: Die):
        self.rolls = rolls
        self.total = total
        self.dice_string = dice_string
        self.die = die


class Operator():
    """Handles creating operators for use in rolls.

    ...

    Attributes
    ----------
    char : str
        character for operand
    regex : str
        raw string, by default just detects the character

    Functions
    -------
    parse - Take the string and output operator and operands
    evaluate - Blank method where the operator is processed

    """
    priority = 0
    char = r""

    @classmethod
    def evaluate(cls, results: list, operand: int, die: Die):
        """
        Evaluate the given dice.

        Args:
            cls: (callable): The class
            dice: (Die): The Die being rolled
        """


class LeftHandOperator(Operator):
    """Operators that act on the object to the left, using the object on the right, inherits from Operator.

    Attributes
    ----------
    operand : str
        The arguments taken by the operator

    """
    operand = r"\d*"


class GreaterThan(LeftHandOperator):
    """Takes an operand and calculates how many die greater than the targetthere have been."""
    priority = 7
    char = r"\>"

    @classmethod
    def evaluate(cls, roll: list, operand: int, die: Die):
        """
        Evaluate a list of results.

        Args:
            cls: (callable): The Class
            results: (list): List of Results.
            operand: (int): The threshold after which die count as success.
            die: (Die): The Die roll.
        """
        logger.debug("Evaluating GreaterThan!")
        for d in roll.rolls:
            if d.value > int(operand):
                d.is_successful = True


class LessThan(LeftHandOperator):
    """Takes an operand and calculates how many die less than the target there have been."""
    priority = 7
    char = r"\<"

    @classmethod
    def evaluate(cls, roll: RollResult, operand: int, die: Die):
        """
        Evaluate a list of results.

        Args:
            cls: (callable): The Class
            results: (list): List of Results.
            operand: (int): The threshold after which die count as success.
            die: (Die): The Die roll.
        """
        logger.debug("Evaluating LessThan!")
        for d in roll.rolls:
            if d.value < int(operand):
                d.is_successful = True


class Exploding(LeftHandOperator):
    """
    Takes dice results, and if the value is greater than the threshold, rolls another die.
    """
    priority = 2
    char = r"x"

    @classmethod
    def evaluate(cls, roll: RollResult, operand: int, die: Die):
        """
        Evaluate the objective function.

        Args:
            cls: (callable): The class
            results: (list): The list of results
            operand: (int): The threshold at which the die is rerolled
            die: (Die): The Die being rolled
        """
        eval_results = []
        for d in roll.rolls:
            value = d.value
            if value >= operand:
                d.is_exploded = True
                new_roll = d
                eval_results.append(d)
                while new_roll.value >= operand:
                    # math.ceil(random.random() * die.sides)
                    new_roll = Result(math.ceil(random.random() * die.sides))
                    if new_roll.value >= operand:
                        new_roll.is_exploded = True
                    eval_results.append(new_roll)
                continue
            else:
                eval_results.append(d)

        roll.rolls = eval_results


class DropLowest(LeftHandOperator):
    """
    Takes a set of dice and returns the highest X of the set
    """
    priority = 1
    char = r"dl"

    @classmethod
    def evaluate(cls, roll: RollResult, operand: int, die: Die):
        logger.debug("Evaluating Keep High!")
        temporary_results = roll.rolls
        for o in range(operand):
            lowest = None
            for index, d in enumerate(temporary_results):
                logger.debug("D is %i", d.value)
                if lowest is None:
                    lowest = index
                    logger.debug("Initializing loop!")
                    continue
                if d.value < temporary_results[lowest].value:
                    lowest = index
                    logger.debug("New lowest: %i", index)
            logger.debug("Dropped: %i", temporary_results[lowest].value)
            temporary_results.pop(lowest)
        roll.rolls = temporary_results


class DropHighest(LeftHandOperator):
    """
    Takes a set of dice and returns the highest X of the set
    """
    priority = 1
    char = r"dh"

    @classmethod
    def evaluate(cls, roll: RollResult, operand: int, die: Die):
        logger.debug("Evaluating Keep High!")
        temporary_results = roll.rolls
        for o in range(operand):
            highest = None
            for index, d in enumerate(temporary_results):
                logger.debug("D is %i", d.value)
                if highest is None:
                    highest = index
                    logger.debug("Initializing loop!")
                    continue
                if d.value > temporary_results[highest].value:
                    highest = index
                    logger.debug("New highest: %i", d.value)
            logger.debug("Dropped: %i", temporary_results[highest].value)
            temporary_results.pop(highest)

        roll.rolls = temporary_results
