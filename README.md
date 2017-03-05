Text for project submission
===========================

According to a study commissioned by the Department of Commerce's National Institute of Standards and Technology (NIST), software bugs are so prevalent that they cost the US economy $59.1 billion annually, or about 0.6% of the gross domestic income [1].
The impact of software bugs on the performance of the global economy and the product development cycle can be expected to increase further, as computer aided design (CAD) and automation will increasingly replace traditional workflows in the near future.
Coming from an aerospace background, an industry that heavily relies on numerical simulations for product development, we decided to work towards a tool to identify software bugs in both, proprietary and open-source software.
The working principle of our software can be best described by an example: suppose an engineer uses a CAD software to design the heat shield of a space craft for atmospheric reentry.
The essential design parameter is the heat distribution in the heat shield, which can be calculated by solving a complicated mathematical equation numerically.
The engineer decides to use a proprietary CAD software to calculate the heat distribution and might obtain a result as shown in the first figure.
From naked eye it is not possible to tell whether or not this solution is correct and as the CAD software is proprietary there is no way to look at the internal wokring of the source code.
Our tool mitigates this problem in the following way: the engineer generates data using the CAD software as described above.
Then, she provides the mathematical equation that governs the heat diffusion and the generated data to our software.
Our software parses the mathematical expression (which is given in a synthax similar to Mathematica) and transforms it in a form suitable for cmputation.
It then evaluates this expression with the given data and checks if the data satisfies the mathematical expression at any point in space and time.
This way, incorrect data and bugs can be easily identified, as shown in the second plot.


[1] https://www.nist.gov/document-17633
