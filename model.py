import model_big
import model_small

def predict(sentence):
    print(len(sentence))
    if len(sentence) < 100:
        print("Going small")
        return model_small.predict(sentence)
    else:
        print("Going big")
        return model_big.predict(sentence)
