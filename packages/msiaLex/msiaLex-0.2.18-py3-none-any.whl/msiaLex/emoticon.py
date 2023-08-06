import csv
import logging
from os import path

logging.basicConfig(
    level=logging.INFO,
    format='%(process)d | %(levelname)s | %(message)s'
)


# pylint: disable=too-many-locals
def _build_dict_from_csv(csv_path):
    """ Builds the Emoji to Sentiment dictionary from the CSV file. """

    emoji_sentiment_rankings = {}

    with open(csv_path, newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        _header_row = next(csv_reader)
        for row in csv_reader:
            emoji = row[0]
            unicode_codepoint = row[1]
            occurrences = int(row[2])
            position = float(row[3])
            negative = float(row[4])
            neutral = float(row[5])
            positive = float(row[6])
            unicode_name = row[7]
            unicode_block = row[8]
            sentiment_score = float(
                '{:.3f}'.format((positive - negative) / occurrences)
            )

            emoji_sentiment_rankings[emoji] = {
                'unicode_codepoint': unicode_codepoint,
                'occurrences': occurrences,
                'position': position,
                'negative': negative,
                'neutral': neutral,
                'positive': positive,
                'unicode_name': unicode_name,
                'unicode_block': unicode_block,
                'sentiment_score': sentiment_score
            }

    return emoji_sentiment_rankings


def get_emoji_sentiment_rank(emoji):
    """ Returns the Sentiment Data mapped to the specified Emoji. """

    return EMOJI_SENTIMENT_DICT[emoji]


EMOJI_SENTIMENT_DICT = _build_dict_from_csv(
    path.join(
        path.abspath(path.dirname(__file__)),
        'data/Emoji_Sentiment_Data_v2.0.csv'
    )
)
