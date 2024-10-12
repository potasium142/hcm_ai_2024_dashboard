import pickle
import streamlit as st

with open("./test_dict.pkl", "rb") as f:
    fdict = pickle.load(f)

container = st.container()
cols = container.columns(2)

output = []
bin_size = 10
size_left = bin_size
cb = []

output_count = 0

og_count = 0
for b in fdict:
    bin_len = len(b[1])
    og_count += bin_len
    cols[0].write(b)

    if (bin_len > size_left):
        if size_left != bin_size:
            output.append(cb)

            for a in cb:
                output_count += len(a[1])

            size_left = bin_size
            cb = []

    if bin_len <= size_left:
        cb.append(b)
        size_left -= bin_len
        continue
    else:
        split_chunk, _ = divmod(bin_len, bin_size)

        for j in range(split_chunk+1):
            start_range = j * bin_size

            splited_bin = [b[0],[b[0], b[1][start_range:start_range+bin_size]]]
            output.append(splited_bin)
        size_left = bin_size


print(og_count, output_count)

cols[1].write(output)
