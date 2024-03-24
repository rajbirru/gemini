def get_response_template():
    return """
Please provide your financial advice in the following format:

Recommended Portfolio:
| Asset | Type | Weight |
|-------|------|--------|
| [Asset 1] | [Stock/ETF/Mutual Fund] | [Weight 1]% |
| [Asset 2] | [Stock/ETF/Mutual Fund] | [Weight 2]% |
| [Asset 3] | [Stock/ETF/Mutual Fund] | [Weight 3]% |
| [Asset 4] | [Stock/ETF/Mutual Fund] | [Weight 4]% |
| [Asset 5] | [Stock/ETF/Mutual Fund] | [Weight 5]% |
| [Asset 6] | [Stock/ETF/Mutual Fund] | [Weight 6]% |
| [Asset 7] | [Stock/ETF/Mutual Fund] | [Weight 7]% |
| [Asset 8] | [Stock/ETF/Mutual Fund] | [Weight 8]% |
| [Asset 9] | [Stock/ETF/Mutual Fund] | [Weight 9]% |
| [Asset 10] | [Stock/ETF/Mutual Fund] | [Weight 10]% |
| Total | | 100% |

Stock/Bond Split:
Based on the client's age of {age} and risk profile of {risk_profile}, the recommended stock/bond split is:
- Stocks: {stock_percentage}%
- Bonds: {bond_percentage}%

Ensure that the total weight of all assets adds up to exactly 100%. Double-check the weights to confirm they sum to 100%.

Explanation:
[Provide a brief explanation of your recommended portfolio and the rationale behind the asset selections and weightings. Consider the client's age, retirement age, and risk profile in your explanation. Discuss how the combination of stocks, ETFs, and mutual funds helps achieve a well-diversified portfolio suited to the client's needs and goals. Explain how the stock/bond split is determined based on the client's age and risk profile, and how it aims to balance growth potential and stability in the portfolio.]
"""