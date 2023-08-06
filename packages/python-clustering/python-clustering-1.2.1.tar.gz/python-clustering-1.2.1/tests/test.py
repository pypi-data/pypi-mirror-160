from asyncio import tasks
import python_clustering


def main():
    print(dir(python_clustering))
    dataset = python_clustering.Dataset()
    dataset_list = ["atom", "D31", "cpu", "banana", "gaussians1", "circle"]
    # assert(dataset.list() == dataset_list)
    data = dataset.load("D31")
    print(data.shape)
    data = dataset.load("D3aa1")
    print(data)
    data = dataset.load("blobs")
    print(data)
    data = dataset.load("blobs", download=True)
    print(data)
    dataset.download("rings")
    description = dataset.load_description("blobs")
    print(description)
    stats = dataset.load_stats("rings")
    print(stats)
    dataset.update_local_info_files()

    tasks = python_clustering.Tasks()
    data = dataset.load("D31").values
    anomalies, methods_results = tasks.detect_anomalies(data)

main()
