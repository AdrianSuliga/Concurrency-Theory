package org.philosophers.utils;

import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartUtils;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.data.category.DefaultCategoryDataset;

import java.io.*;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Stream;

public class GraphGenerator {

    public GraphGenerator() {

    }

    public void generateForNPhilosophers(String path, int n) {
        makeAndSaveChart(readCsvFile(path + n + "_philosophers/philosopher_n", n), path + n + "_philosophers/");
    }

    public void generateForAllVariants() {
        List<List<Double>> averages = new ArrayList<>(Arrays.asList(null, null, null, null));

        for (int n = 5; n < 21; n += 5) {
            int idx = (n / 5) - 1;
            while (averages.size() <= idx) {
                averages.add(new ArrayList<>());
            }

            List<Double> current = new ArrayList<>();

            for (int j = 1; j <= 6; j++) {
                current.add(readCsvFile("src/main/resources/version" + j + "/" + n + "_philosophers/philosopher_n", n).getLast());
            }

            averages.set(idx, current);
        }

        DefaultCategoryDataset dataset = new DefaultCategoryDataset();

        for (int i = 0; i < averages.getFirst().size(); i++) {
            String variant = "Variant " + (i + 1);
            dataset.addValue(averages.getFirst().get(i), "N = 5", variant);
            dataset.addValue(averages.get(1).get(i), "N = 10", variant);
            dataset.addValue(averages.get(2).get(i), "N = 15", variant);
            dataset.addValue(averages.get(3).get(i), "N = 20", variant);
        }

        JFreeChart chart = ChartFactory.createBarChart(
                "Simulation",
                "Variants",
                "Times [ms]",
                dataset,
                PlotOrientation.VERTICAL,
                true,
                true,
                false
        );

        try {
            File file = new File("src/main/resources/graph.png");
            file.getParentFile().mkdirs();
            ChartUtils.saveChartAsPNG(file, chart, 800, 600);
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
    }

    private void makeAndSaveChart(List<Double> average_times, String path) {
        DefaultCategoryDataset dataset = new DefaultCategoryDataset();

        for (int i =  0; i < average_times.size() - 1; i++) {
            dataset.addValue(average_times.get(i), "philosophers", "P" + (i + 1));
        }
        dataset.addValue(average_times.getLast(), "philosophers", "AVG");

        JFreeChart chart = ChartFactory.createBarChart(
                "Average Time = " + average_times.getLast() + " ms",
                "Philosophers",
                "Time [ms]",
                dataset
        );

        try {
            File file = new File(path + "graph.png");
            file.getParentFile().mkdirs();
            ChartUtils.saveChartAsPNG(file, chart, 800, 600);
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
    }

    private List<Double> readCsvFile(String path, int n) {
        int global_sum = 0, global_cnt = 0;

        List<Double> average_times = new ArrayList<>();

        for (int i = 1; i <= n; i++) {
            File file = new File(path + i + ".csv");

            try {
                List<String> lines = Files.readAllLines(file.toPath());
                if (!lines.isEmpty()) {
                    lines.removeFirst();
                }

                int sum = 0, cnt = 0;
                for (String line : lines) {
                    sum += Integer.parseInt(line.trim());
                    cnt++;
                }

                global_sum += sum;
                global_cnt += cnt;

                average_times.add((double)Math.round(cnt == 0 ? 0.0 : (double) (sum * 100) / cnt) / 100);
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        }

        average_times.add((double)Math.round((double)(global_sum * 100) / global_cnt) / 100);

        return average_times;
    }

}
