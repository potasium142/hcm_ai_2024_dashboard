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


def group_occurence(indices: np.ndarray
                    ) -> tuple[np.ndarray, np.ndarray]:
    return np.unique(indices, return_counts=True)


def group_by_occurence(results) -> dict:
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
    return output


def paging(results, k):
    i = 0
    output = []

    f_page = []
    for b in results:
        f = b[1]
        bin_size = len(f)

        remain_size = k - i

        if bin_size < remain_size:
            i = i+bin_size
            f_page.append([b[0], f])
            continue

        f_page.append([b[0], f[:remain_size]])

        output.append(f_page)
        f_page = []

        new_bin = f[remain_size:]

        split_chunk, i_a = divmod(len(new_bin), k)

        for j in range(split_chunk+1):
            start_range = i + k*(j)
            end_range = i+k*(j+1)
            f_page.append([b[0], new_bin[start_range: end_range]])

            output.append(f_page)
            f_page = []

        i = i_a

    if len(f_page) > 0:
        output.append(f_page)

    return output
