import os
import yaml

rootDir = os.path.dirname(os.getcwd())


def readScoresFile():
    with open(os.path.join('data', 'scores.yaml')) as file:
        scoresFile = yaml.load(file, Loader=yaml.FullLoader)

    return scoresFile


def writeScoresFile(player: str, score: int):
    scoreFile = readScoresFile()
    scoreFile['highscore']['player'] = player
    scoreFile['highscore']['score'] = score

    with open(os.path.join('data', 'scores.yaml'), 'w') as file:
        yaml.dump(scoreFile, file)