T1
# Claim: the two groups used the same amount of data before the offer
# H₀: Both groups have the same true average daily data before May
# H₁: the two averages differ

  F-test:
  F = 0.9003
  p = 5.673 * 10⁻⁴
  Decision: Variances differ.

 Z-test:
 Z = -0.5191
 p = 0.6037 which >0.05

 Decision
 Fail to reject H₀.

 Conclusion
 There is insufficient evidence that the groups differed in their average daily data usage before the offer.
 The groups are considered balanced on this important pre-offer measure.

T2
F-test:
- F = Check output
- p = Check output
- Decision: Check whether variances differ.

2-test:
- Z = Check output
- p > 0.05
Decision:
Fail to reject H₀.

Conclusion:
There is no statistically significant difference in the average revenue between Group A and Group B before the offer. Therefore, we fail to reject H₀.

T3
Z-test:
- Z = 2.5457
- p = 0.0109

Decision:
p = 0.0109 which is less than 0.05.
Reject H₀

Conclusion:
There is a statistically significant difference in the proportion of smartphone users between Group A and Group B.

T4
F-test:
F = Run f_test(A, B) output

p = Run output

Decision: Check whether variances differ.

Z-test:
Z = Run z_mean2(B, A) output

p = Run output

Decision:
- p < 0.05 → Reject H₀.
- p > 0.05 → Fail to reject H₀.

Conclusion:
If p is less than 0.05, there is sufficient statistical evidence that Group B has higher average daily data usage than Group A.

T5
F-test:
- F = f_test(b,a) output
- p = Output value

- Decision: Check whether variances differ.

T-test:
- t = Output value
- p = Output value

Decision:
- p < 0.05 → Reject H₀.
- p > 0.05 → Fail to reject H₀.

Conclusion:
If p < 0.05:

There is sufficient statistical evidence that Group B paid more on average than Group A. Therefore, the offer significantly increased revenue.

T6
Z-test:
- Z = Check output
- p-value < 0.05

Decision:
Reject H₀
Since the p-value is less than 0.05, the result is statistically significant.

Conclusion:
There is sufficient statistical evidence that prepaid and postpaid subscribers have different churn rates. Therefore, we reject the null hypothesis (H₀).

T7
Z-test:
- Z = Check output
- p-value < 0.05

Decision:
Reject H₀
Since the p-value is less than 0.05, the result is statistically significant.

Conclusion:
There is sufficient statistical evidence that subscribers with open tickets have a different churn rate compared to subscribers who never complained. Therefore, we reject the null hypothesis (H₀).

T8
Z-test:
- Group A: 1328 / 4610
- Group B: 632 / 3374
- Z = Check output
- p-value < 0.05

Decision:
Reject H₀
Since the p-value is less than 0.05, the result is statistically significant.

Conclusion:
There is sufficient statistical evidence that Year-0 and Year-3 subscribers have different churn rates. Therefore, we reject the null hypothesis (H₀).

T9
Z-test:
- Himachal Pradesh: 417 / 1247
- Punjab: 77 / 558
- Z = Check output
- p-value < 0.05

Decision:
Reject H₀
Since the p-value is less than 0.05, the result is statistically significant.

Conclusion:
There is sufficient statistical evidence that Himachal Pradesh and Punjab subscribers have different churn rates. Therefore, we reject the null hypothesis (H₀).

T10
Z-test:
- Smartphone: 4507 / 18971
- Feature-phone: 719 / 3029
- Z = Check output
- p-value > 0.05

Decision:
Fail to reject H₀
Since the p-value is greater than 0.05, the result is not statistically significant.

Conclusion:
There is insufficient statistical evidence to conclude that smartphone and feature-phone users have different churn rates. Therefore, we fail to reject the null hypothesis (H₀).

T11
Decision
- p < 0.05 → Reject H₀.
- p > 0.05 → Fail to reject H₀.

Conclusion
If p < 0.05, there is a statistically significant difference in average daily data usage between the groups.
One correction bro: dev query customer-wise average calculate cheyyunnathaanu. Gender/device comparison-inu gen use cheyyam.

T12
F-test
- Groups compared: Female vs Male
- p-value < 0.05
- Result: Significant difference in variances.

Z-test (Mean)
- Groups compared: Female vs Male
- p-value < 0.05

- Result: Significant difference in average daily data usage.

Decision
Reject H₀

Conclusion
There is sufficient statistical evidence to conclude that male and female subscribers have different average daily data usage.

T13
F-test
Groups compared: Feature Phone vs Smartphone.

Test: F-test for variance comparison.
p-value: Less than 0.05.
Decision: Variances differ significantly.

Z-test
Test: Two-sample Z-test.

Comparison: Average daily data usage of Feature Phone and Smartphone users.

p-value: Less than 0.05 (as indicated by the decision).

Decision
Reject H₀.

Conclusion
There is sufficient statistical evidence to conclude that Smartphone users have a higher average daily data usage than Feature Phone users.

T14
Group Comparison
No complaints: 6,680 subscribers, 1,834 churned.

Complaints: 6,631 subscribers, 1,328 churned.

Z-proportion Test

Test: Two-sample Z-test for proportions.
No complaints churn rate: 27.46%.
Complaints churn rate: 20.03%.

Z-statistic: Approximately 10.06.
P-value: Less than 0.05.

Decision
Reject H₀.

Conclusion
There is sufficient statistical evidence to conclude that subscribers with complaints and subscribers without complaints have significantly different churn rates. Subscribers without complaints have a higher observed churn rate than subscribers with complaints.

T15
Group Comparison
No Roaming: 16,233 subscribers, 2,653 churned.
Roaming: 5,767 subscribers, 2,573 churned.

Z-proportion Test

Test: Two-sample Z-test for proportions.
No Roaming churn rate: 16.34%.
Roaming churn rate: 44.61%.

Z-statistic: Approximately -43.4.

P-value: Less than 0.05.

Decision
Reject H₀.

Conclusion
There is sufficient statistical evidence to conclude that subscribers with roaming activity and subscribers without roaming activity have significantly different churn rates. Subscribers with roaming activity have a much higher observed churn rate than subscribers without roaming activity.
