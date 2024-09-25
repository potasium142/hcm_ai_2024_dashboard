import numpy as np


def group_by_video(results):
    gr = dict()
    for d in results:
        index = d[2].item() * 1000 + d[3].item()

        vid_bin = gr.get(index, list())

        vid_bin.append(d)

        gr[index] = vid_bin

    return sorted(
        gr.items(),
        key=lambda x: len(x[1]),
        reverse=True
    )


def group_by_conf(results) -> dict:
    conf_bin = dict()

    # for result in results:
    for f in results:
        fbin = conf_bin.get(f[0], list())
        fbin.append(f)
        conf_bin[f[0]] = fbin

    return sorted(
        conf_bin.items(),
        key=lambda x: x[0],
        reverse=True
    )


def get_nearby(results,
               k,
               frame_index_list):

    output = list()
    # for result in results:

    #     near_frames_list = list()
    for f in results:
        flist = frame_index_list[f[2]-1][f[3]-1]

        for i in range(-k, k+1):
            index = f[1] + i
            try:
                output.append([
                    f[0],
                    index,
                    f[2],
                    f[3],
                    flist[index]
                ])
            except:
                pass
    # output.append(near_frames_list)

    return output
