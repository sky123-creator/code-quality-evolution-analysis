from pipeline.batch_processor import process_all_projects
from pipeline.csv_exporter import export_to_csv

CONFIG = {
    "project_root": "./data/use",
    "output_csv": "./results/project_metrics.csv"
}

def main():
    print("开始执行数据流水线")
    all_metrics = process_all_projects(CONFIG["project_root"])
    export_to_csv(all_metrics, CONFIG["output_csv"])
    print("流水线执行完成")

if __name__ == "__main__":
    main()