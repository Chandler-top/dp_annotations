from supar import Parser
import os
#通过语义依存的文件解析生成句法依存的文件
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
    semheads = []
    semdeprels = []
    bios = []
    sentence = []

    for line in fsrc:
        if (len(line) == 0 or line == '\n' or line == '\t\n') and len(sentence) !=0:
            #semdp = parser.predict([sentence], prob=True, verbose=False)
            syndp = parser.predict([sentence], verbose=False)
            synheads = syndp.sentences[0].values[6]
            deprels = syndp.sentences[0].values[7]
            idx = 1
            for w, l, p, pp, f, syh, sydep, sypdep, pre, smh, smdep, b in \
                    zip(words, lemmas, poses, pposes, feats, synheads, deprels, pdeprels,
                        preds, semheads, semdeprels, bios):
                fsdp.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(idx, w, l, p, pp, f,
                                                                                       syh, sydep, sypdep, pre, smh, smdep, b))
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
            semheads = []
            semdeprels =[]
            bios = []
            sentence = []
            continue
        elif line != '\n':
            splits = line.split('\t')
            word = splits[1]
            lemma = '-'
            pos = splits[2]
            ppos = splits[2]
            feat = '-'
            synhead = '-'
            deprel = '-'
            pdeprel = '-'
            pred = '-'
            semhead = splits[10]
            semprel = splits[11]
            bio = splits[12]

            words.append(word)
            lemmas.append(lemma)
            poses.append(pos)
            pposes.append(ppos)
            feats.append(feat)
            synheads.append(synhead)
            deprels.append(deprel)
            pdeprels.append(pdeprel)
            preds.append(pred)
            semheads.append(semhead)
            semdeprels.append(semprel)
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
                "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(idx, w, l, p, pp, f,
                                                                                       syh, sydep, sypdep, pre, smh, smdep, b))
            idx += 1

    fsdp.close()
    fsrc.close()

if __name__ == "__main__":
    file = "/Users/shawn/Documents/天大博士/projects/supar-ontonotes/parser-main/exp/ptb.biaffine.dep.roberta"
    parser = Parser.load(file)
    gen_semdp('./conll2003/dev.conll2003.dm.conllx', './conll2003/dev.sd.conllx')
    gen_semdp('./conll2003/test.conll2003.dm.conllx', './conll2003/test.sd.conllx')
    gen_semdp('./conll2003/train.conll2003.dm.conllx', './conll2003/train.sd.conllx')

#python vi_semantic_dependency.py train -f tag,char,lemma -b --max-len 256 -p exp/vi.semantic.sdp.pas.bert -d 0 --epochs 100
