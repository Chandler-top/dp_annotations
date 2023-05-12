from supar import Parser
import os

def splitsdp(sdpstr:str):
    sdpindex = []
    sdplabel = []
    for i in range(len(sdpstr)):
        sdp = sdpstr[i]
        if sdp == '_':
            sdpindex.append('_')
            sdplabel.append('_')
            continue
        sdp = sdpstr[i].split('|')
        subsdpindex = []
        subsdplabel = []
        for j in range(len(sdp)):
            subsdp = sdp[j].split(':')
            subsdpindex.append(subsdp[0])
            subsdplabel.append(subsdp[1])
        sdpindex.append(",".join([str(x) for x in subsdpindex]))
        sdplabel.append(",".join([str(x) for x in subsdplabel]))
    return sdpindex, sdplabel


def gen_semdp(filename:str, out:str):
    fsrc = open(filename,'r', encoding='utf-8')
    fsdp = open(out, 'w', encoding='utf-8')

    words = []
    lemmas = []
    poses = []
    pposes = []
    feats = []
    synheads = []
    deprels = []
    pdeprels = []
    preds = []
    bios = []
    sentence = []

    for line in fsrc:
        if (len(line) == 0 or line == '\n' or line == '\t\n') and len(sentence) !=0:
            #semdp = parser.predict([sentence], prob=True, verbose=False)
            syndp = parser.predict([sentence], verbose=False)
            synheads = syndp.sentences[0].values[6]
            deprels = syndp.sentences[0].values[7]
            idx = 1
            for w, l, p, pp, f, syh, sydep, sypdep, pre, b in \
                    zip(words, lemmas, poses, pposes, feats, synheads, deprels, pdeprels, preds, bios):
                fsdp.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(idx, w, l, p, pp, f, syh, sydep, sypdep, pre, b))
                idx += 1
            fsdp.write('\n')
            words = []
            lemmas = []
            poses = []
            pposes = []
            feats = []
            synheads = []
            deprels = []
            pdeprels = []
            preds = []
            bios = []
            sentence = []
            continue
        elif line != '\n':
            splits = line.split(' ')
            word = splits[0]
            lemma = '-'
            pos = splits[1]
            ppos = splits[1]
            feat = splits[2]
            synhead = '-'
            deprel = '-'
            pdeprel = '-'
            pred = '-'
            bio = splits[3]

            words.append(word)
            lemmas.append(lemma)
            poses.append(pos)
            pposes.append(ppos)
            feats.append(feat)
            synheads.append(synhead)
            deprels.append(deprel)
            pdeprels.append(pdeprel)
            preds.append(pred)
            bios.append(bio)
            sentence.append(word)

    if len(sentence) > 0:
        #semdp = parser.predict([sentence], prob=True, verbose=False)
        syndp = parser.predict([sentence], verbose=False)
        synheads = syndp.sentences[0].values[6]
        deprels = syndp.sentences[0].values[7]
        idx = 1
        for w, l, p, pp, f, syh, sydep, sypdep, pre, b in \
                zip(words, lemmas, poses, pposes, feats, synheads, deprels, pdeprels, preds, bios):
            fsdp.write(
                "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(idx, w, l, p, pp, f, syh, sydep, sypdep, pre, b))
            idx += 1

    fsdp.close()
    fsrc.close()

if __name__ == "__main__":
    file = "./model/ptb.biaffine.dep.lstm.char" #en: ptb.biaffine.dep.lstm.char, es / ca: ud.biaffine.dep.xlmr, cn: ctb7.biaffine.dep.lstm.char
    parser = Parser.load(file)
    # parser = Parser.load('dep-biaffine-en')
    dataset = parser.predict([['Three', 'of', 'Grace', 'Energy', '\'s', 'seven', 'board',
                               'seats', 'are', "held", 'by', 'W.R.', 'Grace', '.']], prob=True, verbose=False)
    print(dataset.sentences[0])
    gen_semdp('./conll2003/train.txt', './conll2003/train.supar.conllx')
    gen_semdp('./conll2003/dev.txt', './conll2003/dev.supar.conllx')
    gen_semdp('./conll2003/test.txt', './conll2003/test.supar.conllx')

#python vi_semantic_dependency.py train -f tag,char,lemma -b --max-len 256 -p exp/vi.semantic.sdp.pas.bert -d 0 --epochs 100
