Text for project submission
===========================

According to a study commissioned by the Department of Commerce's National Institute of Standards and Technology (NIST), software bugs are so prevalent that they cost the US economy $59.1 billion annually, or about 0.6% of the gross domestic income [1].
The impact of software bugs on the performance of the global economy and the product development cycle can be expected to increase further, as computer aided design (CAD) and automation increasingly replace traditional workflows.
Coming from an aerospace background, an industry that heavily relies on numerical simulations for product development, we built a tool to identify software bugs in both proprietary and open-source software.

The working principle of our software is best described by an example: suppose an engineer uses a CAD software to design the heat shield of a Mars lander for planetary entry.
The essential design parameter is the heat distribution in the heat shield, which can be calculated by solving a complicated mathematical equation numerically.
The engineer decides to use a proprietary CAD software to calculate the heat distribution and might obtain a result as shown in the first figure.
From the naked eye it is not possible to tell whether or not this solution is correct and as the CAD software is proprietary there is no way to look at the internal working of the source code.
NuVe mitigates this problem in the following way: the engineer generates data using the CAD software as described above.
Then, she provides the mathematical equation that governs the heat diffusion and the generated data to our software.
NuVe parses the mathematical expression (which is given in a syntax similar to Mathematica) and transforms it to a form suitable for computation.
It then evaluates this expression with the given data and checks if the data satisfies the mathematical expression at any point in space and time.

NuVe identifies incorrect data and therefore bugs, as shown in the last plot.

**One of these datasets is correct and the other is not, but the difference is hard to detect.**
![correct_data_2d](https://cloud.githubusercontent.com/assets/26180580/23590232/07ff0fbe-0191-11e7-8b12-88862096b391.png)

![incorrect_data_2d](https://cloud.githubusercontent.com/assets/26180580/23590229/07b0e406-0191-11e7-9a05-f9f1d5a2d978.png)

**NuVe easily identifies the erroneous data.**
![error_2d](https://cloud.githubusercontent.com/assets/26180580/23590231/07cf2178-0191-11e7-8d90-33b7a0f31c8b.png)

[1] https://www.nist.gov/document-17633
