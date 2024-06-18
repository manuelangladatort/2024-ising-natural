import random
from dominate import tags

from psynet.demography.general import Age, Gender
from psynet.demography.gmsi import GMSI
from psynet.modular_page import ModularPage, TextControl, SurveyJSControl
from psynet.page import InfoPage
from psynet.timeline import join, FailedValidation


def introduction():
    html = tags.div()
    with html:
        tags.p(
            "Congratulations, you completed the main experiment!"
        )
        tags.p(
            "Before we finish, we would like to ask you a few questions about you. ",
            "They should only take a couple of minutes to complete.",
        )
    return InfoPage(html, time_estimate=10)


def questionnaire():
    return join(
        introduction(),
        Age(),
        Gender(),
        GMSI(subscales=["Musical Training"]),
        feedback(),
    )


STOMPR_rating_values = [
    {"value": "1", "text": "1 (Dislike Strongly)"},
    {"value": "2", "text": "2"},
    {"value": "3", "text": "3"},
    {"value": "4", "text": "4"},
    {"value": "5", "text": "5"},
    {"value": "6", "text": "6"},
    {"value": "7", "text": "7 (Like Strongly)"}
]

music_genres = [
    {"value": "Alternative", "text": "Alternative"},
    {"value": "Bluegrass", "text": "Bluegrass"},
    {"value": "Blues", "text": "Blues"},
    {"value": "Classical", "text": "Classical"},
    {"value": "Country", "text": "Country"},
    {"value": "Dance/Electronica", "text": "Dance/Electronica"},
    {"value": "Folk", "text": "Folk"},
    {"value": "Funk", "text": "Funk"},
    {"value": "Gospel", "text": "Gospel"},
    {"value": "Heavy Metal", "text": "Heavy Metal"},
    {"value": "World", "text": "World"},
    {"value": "Jazz", "text": "Jazz"},
    {"value": "New Age", "text": "New Age"},
    {"value": "Oldies", "text": "Oldies"},
    {"value": "Opera", "text": "Opera"},
    {"value": "Pop", "text": "Pop"},
    {"value": "Punk", "text": "Punk"},
    {"value": "Rap/hip-hop", "text": "Rap/hip-hop"},
    {"value": "Reggae", "text": "Reggae"},
    {"value": "Religious", "text": "Religious"},
    {"value": "Rock", "text": "Rock"},
    {"value": "Soul/R&B", "text": "Soul/R&B"},
    {"value": "Soundtracks/theme song", "text": "Soundtracks/theme song"}
]


class STOMPR(ModularPage):
    def __init__(self):
        super().__init__(
            "stompr",
            "Rate your preferences for each music genre on a scale from 1 (Dislike Strongly) to 7 (Like Strongly). You will earn 0.15 dollars.",
            SurveyJSControl(
                {
                    "logoPosition": "right",
                    "pages": [
                        {
                            "name": "page1",
                            "elements": [
                                {
                                    "type": "matrix",
                                    "name": "STOMPR_choices",
                                    "title": "Please indicate your basic preference for each of the following genres using the scale provided.",
                                    "isRequired": True,
                                    "columns": STOMPR_rating_values,
                                    "rows": music_genres,
                                },
                            ],
                        },
                    ],
                },
            ),
            time_estimate=55,
            bot_response=lambda: {"rating": "5",},
        )

    def validate(self, response, **kwargs):
        n_responses = len(response.answer["STOMPR_choices"])

        if n_responses < len(music_genres):
            return FailedValidation("Please answer all the questions.")

        return None


TIPI_rating_values = [
    {"value": "1", "text": "1 (Disagree Strongly)"},
    {"value": "2", "text": "2"},
    {"value": "3", "text": "3"},
    {"value": "4", "text": "4"},
    {"value": "5", "text": "5"},
    {"value": "6", "text": "6"},
    {"value": "7", "text": "7 (Agree Strongly)"}
]

tipi_genres = [
    {"value": "Extraverted", "text": "Extraverted, enthusiastic"},
    {"value": "Critical", "text": "Critical, quarrelsome."},
    {"value": "Dependable", "text": "Dependable, self-disciplined."},
    {"value": "Anxious", "text": "Anxious, easily upset."},
    {"value": "Open", "text": "Open to new experiences, complex."},
    {"value": "Reserved", "text": "Reserved, quiet."},
    {"value": "Sympathetic", "text": "Sympathetic, warm."},
    {"value": "Disorganized", "text": "Disorganized, careless."},
    {"value": "Calm", "text": "Calm, emotionally stable."},
    {"value": "Conventional", "text": "Conventional, uncreative."},
]

class TIPI(ModularPage):
    def __init__(self):
        super().__init__(
            "tipi",
            "Here are a number of personality traits that may or may not apply to you. Please rate each statement to indicate the extent to which you agree/ disagree with them on a scale from 1 (Disagree Strongly) to 7 (Agree Strongly). You will earn 0.15 dollars.",
            SurveyJSControl(
                {
                    "logoPosition": "right",
                    "pages": [
                        {
                            "name": "page1",
                            "elements": [
                                {
                                    "type": "matrix",
                                    "name": "TIPI_choices",
                                    "title": "I see myself as:",
                                    "isRequired": True,
                                    "columns": TIPI_rating_values,
                                    "rows": tipi_genres,
                                },
                            ],
                        },
                    ],
                },
            ),
            time_estimate=55,
            bot_response=lambda: {"rating": "5",},
        )

    def validate(self, response, **kwargs):
        n_responses = len(response.answer["TIPI_choices"])

        if n_responses < len(tipi_genres):
            return FailedValidation("Please answer all the questions.")

        return None


def feedback():
    return ModularPage(
        "feedback",
        "Do you have any feedback to give us about the experiment?",
        TextControl(one_line=False),
        bot_response="I am just a bot, I don't have any feedback for you.",
        save_answer="feedback",
        time_estimate=5,
    )


def debrief():
    html = tags.div()

    with html:
        tags.p(
            """
            Thank you for participating in this experiment. The purpose of the experiment was to collect data on how we 
            perceive ‘pleasant’ melodies (sequences of musical tones), such as the ones you have been listening to.
            """
        )
        tags.p(
            """
            Pleasantness is very important to understand how we perceive and create musical melodies (the main musical 
            idea in a piece of music, or that part that you can sing or hum along to). Other important aspects melodies 
            are pitch (the series of notes that rise and fall in pitch) and rhythm (the timing and duration of these 
            notes).
            """
        )
        tags.p(
            """
            The data collected during this experiment will help to better understand how people derive pleasure from 
            melodies, studying for the first time all possible melodic combinations and listeners' individual 
            differences at a large scale (testing many melodies and participants from different backgrounds).
            """
        )

    return InfoPage(html, time_estimate=10)
