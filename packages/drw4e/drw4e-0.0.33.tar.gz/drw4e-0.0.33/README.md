<p>This package, drw4e, is a tool to fit a damped random walk model on a 
single-band AGN light curve with four different types of measurement error. 
A typical damped random walk process (Kelly et al., 2009) is built on a 
Gaussian measurement error. Tak et al. (2019) adopts a mixture of Gaussian 
and Student's t measurement errors to account for the effect of outlying 
observations. In addition to these two types of measurement error, 
drw4e provides two more types of measurement error; a mixture of two 
Gaussian measurement errors (Vallisneri and van Haasteren, 2017) and 
Student's t measurement error. 

The common outputs of drw4e are the posterior samples of the three 
damped random walk model parameters; (i) average magnitude, 
(ii) short-term variability, and (iii) time scale. The last two 
model parameters are known to have physical interpretations 
(Kelly et al., 2009) empirically supported by numerous studies 
(MacLeod et al., 2010; Kozlowski et al., 2010;  Kim et al., 2012; 
and Andrae et al., 2013). Thus, obtaining their accurate estimates 
has become an important data analytic problem in astronomy. 
The Gaussian measurement error model outputs posterior samples of these 
three parameters. When a measurement error involves Student's t distribution,
such as Student's t or a mixture of Gaussian and Student's t distributions,
this package would optionally provide a posterior sample of degrees of freedom 
of Student's t distribution if the degrees of freedom were treated as an unknown 
parameter to be estimated from the data. In addition, the two mixture types of 
measurement error (Gaussian + Gaussian and Gaussian + Student's t) 
will provide each measurement's probability of being an outlier, 
which will be helpful for identifying observations that a Gaussian 
measurement error cannot fit well.

This package can also be used for a sensitivity check of the Gaussian measurement
error model, providing variations of the outputs according to different 
measurement error assumptions. In the absence of outliers, the resulting 
posterior distributions under the four types of measurement error are 
supposed to be similar in terms of the shape, center, and variability. 
In the presence of outliers, however, the Gaussian measurement error model
may result in quite different posterior distributions from those of 
the other measurement error models. In this case, the result from the 
Gaussian measurement error model would be severely biased, and thus 
the results obtained by the other three robust measurement error types 
would become more reliable.
</p>

<h2>Installation</h2>
<pre> pip install drw4e</pre>

<h2>Tutorial</h2>
<p>
Each of the following four links leads to a detailed tutorial with a realistic MACHO light curve.
It also contains descriptions of the data and instructions on how to use the package and its output.
<br/><br/>
</p>

<a href="https://github.com/HW0327/drw4e/blob/main/Mixture%20of%20Gaussian%20and%20Student's%20t%20measurement%20error%20model.ipynb">
Using a mixture of Gaussian and Student's t measurement error model
</a>

<a href="https://github.com/HW0327/drw4e/blob/main/A%20Mixture%20of%20Two%20Gaussian%20Measurement%20Error%20Model.ipynb">Using a mixture of two Gaussian measurement error model
</a>

<a href="https://github.com/HW0327/drw4e/blob/main/Gaussian%20measurement%20error%20model.ipynb">Using a Gaussian measurement error model
</a>

<a href="https://github.com/HW0327/drw4e/blob/main/Student's%20t%20measurement%20error%20model.ipynb">Using a Student's t measurement error model
</a>