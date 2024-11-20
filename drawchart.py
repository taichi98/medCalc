import matplotlib.pyplot as plt
import plotly.tools as tls
import pandas as pd
import plotly.graph_objs as go


def draw_bmi_chart(bmi, age_months, sex):
    #Lựa chọn dữ liệu theo giới tinh
    if sex == 1:  # boys
        file_path = 'data/bfa-boys-zscore-expanded-tables.xlsx'
        #title = 'BMI/Age Z-Score for Boys (0-5 years)'
    elif sex == 2:  # girls
        file_path = 'data/bfa-girls-zscore-expanded-tables.xlsx'
        #title = 'BMI/Age Z-Score for Girls (0-5 years)'
    else:
        raise ValueError("Invalid sex. Please use 1 for male or 2 for female.")

    # Đọc dữ liệu từ tệp Excel
    data = pd.read_excel(file_path)

    # Chuyển đổi tuổi từ ngày sang tháng
    age_days = data['Day']
    age_months_data = age_days / 30.4375
    sd3neg = data['SD3neg']
    sd2neg = data['SD2neg']
    sd1neg = data['SD1neg']
    sd0 = data['SD0']
    sd1 = data['SD1']
    sd2 = data['SD2']
    sd3 = data['SD3']

    # Vẽ biểu đồ bằng Matplotlib
    plt.plot(age_months_data, sd3neg, label='-3SD', color='black')
    plt.plot(age_months_data, sd2neg, label='-2SD', color='red')
    plt.plot(age_months_data, sd1neg, label='-1SD', color='#DAA41F')
    plt.plot(age_months_data, sd0, label='Mean', color='green')
    plt.plot(age_months_data, sd1, label='+1SD', color='#DAA41F')
    plt.plot(age_months_data, sd2, label='+2SD', color='red')
    plt.plot(age_months_data, sd3, label='+3SD', color='black')

    # Thêm điểm BMI của trẻ
    plt.scatter(age_months,
                bmi,
                color='red',
                label='Child Data Point',
                zorder=5)

    # Thêm tiêu đề và nhãn
    plt.xlabel('Age (months)', fontsize=10)
    plt.ylabel('BMI (kg/m²)', fontsize=10)

    # Chuyển đổi Matplotlib sang Plotly
    plotly_fig = tls.mpl_to_plotly(plt.gcf())
    # Cập nhật hovertemplate (giới hạn số thập phân)
    plotly_fig.update_traces(
        hovertemplate="%{x:.2f}, %{y:.2f}"
    )
    # Cấu hình trục hoành trong Plotly
    plotly_fig.update_xaxes(tickvals=[0, 12, 24, 36, 48, 60],
                            ticktext=[
                                "Birth", "1 year", "2 years", "3 years",
                                "4 years", "5 years"
                            ],
                            range=[0, 61])
    shapes = [
        dict(
            type="line",
            x0=year * 12,
            y0=sd3neg.min() - 10,
            x1=year * 12,
            y1=sd3.max() + 10,
            line=dict(
                color="gray",
                width=2 if year == 2 else 0.2,  # Nét dày hơn cho year = 2
                dash="solid" if year == 2 else "dash"  # Nét liền cho year = 2
            )) for year in range(1, 6)
    ] + [
        # Trục hoành
        dict(
            type="line",
            x0=age_months_data.min(),
            y0=y,
            x1=age_months_data.max(),
            y1=y,
            line=dict(
                color="gray",
                width=0.2,
                dash="dash"  # Nét đứt
            )) for y in [10, 12, 14, 16, 18, 20, 22]
    ] + [  # Thêm hình chữ nhật làm khung
        dict(
            type="rect",
            xref="paper",
            yref="paper",
            x0=0,
            y0=0,
            x1=1,
            y1=1,
            line=dict(
                color="black",
                width=1,  # Độ dày khung
            ),
        )
    ]
    annotations = [
        dict(
            x=1.001,  # Tọa độ x tính theo tỷ lệ của toàn bộ chiều rộng (2% ngoài phạm vi biểu đồ)
            y=sd3neg.iloc[-1],
            text='-3SD',
            font=dict(color='black', size=8, weight='bold'),
            xref="paper",  # Dùng tỷ lệ trên trục ngang của toàn bộ đồ thị
            yref="y",  # Dựa theo dữ liệu thật trên trục dọc
            showarrow=False,
            xanchor="left"  # Căn chữ về bên trái
        ),
        dict(x=1.001,
             y=sd2neg.iloc[-1],
             text='-2SD',
             font=dict(color='red', size=8, weight='bold'),
             xref="paper",
             yref="y",
             showarrow=False,
             xanchor="left"),
        dict(x=1.001,
             y=sd1neg.iloc[-1],
             text='-1SD',
             font=dict(color='#DAA41F', size=8, weight='bold'),
             xref="paper",
             yref="y",
             showarrow=False,
             xanchor="left"),
        dict(x=1.001,
             y=sd0.iloc[-1],
             text='Mean',
             font=dict(color='green', size=8, weight='bold'),
             xref="paper",
             yref="y",
             showarrow=False,
             xanchor="left"),
        dict(x=1.001,
             y=sd1.iloc[-1],
             text='+1SD',
             font=dict(color='#DAA41F', size=8, weight='bold'),
             xref="paper",
             yref="y",
             showarrow=False,
             xanchor="left"),
        dict(x=1.001,
             y=sd2.iloc[-1],
             text='+2SD',
             font=dict(color='red', size=8, weight='bold'),
             xref="paper",
             yref="y",
             showarrow=False,
             xanchor="left"),
        dict(x=1.001,
             y=sd3.iloc[-1],
             text='+3SD',
             font=dict(color='black', size=8, weight='bold'),
             xref="paper",
             yref="y",
             showarrow=False,
             xanchor="left"),
    ]

    # Cập nhật layout
    plotly_fig.update_layout(
        autosize=True,
        width=none,  # Chiều rộng của biểu đồ
        height=none,  # Chiều cao của biểu đồ
        margin=dict(l=30, r=30, t=20, b=20),  # Điều chỉnh biên
        annotations=annotations,
        plot_bgcolor="white",  # Đổi nền thành màu trắng
        xaxis_title="Age (months)",
        yaxis_title="BMI (kg/m²)",
        shapes=shapes,
    )

    # Chuyển đổi biểu đồ thành JSON
    chart_json = plotly_fig.to_json()
    return chart_json


# Hàm vẽ biểu đồ Weight-for-Age (WFA)
def draw_wfa_chart(weight, age_months, sex):
    # Lựa chọn dữ liệu theo giới tính
    if sex == 1:  # boys
        file_path = 'data/wfa-boys-zscore-expanded-tables.xlsx'
    elif sex == 2:  # girls
        file_path = 'data/wfa-girls-zscore-expanded-tables.xlsx'
    else:
        raise ValueError("Invalid sex. Please use 1 for male or 2 for female.")

    # Đọc dữ liệu từ tệp Excel
    data = pd.read_excel(file_path)

    # Chuyển đổi tuổi từ ngày sang tháng
    age_days = data['Day']
    age_months_data = age_days / 30.4375
    sd3neg = data['SD3neg']
    sd2neg = data['SD2neg']
    sd0 = data['SD0']
    sd2 = data['SD2']
    sd3 = data['SD3']

    # Vẽ biểu đồ bằng Matplotlib
    plt.plot(age_months_data, sd3neg, label='-3SD', color='black')
    plt.plot(age_months_data, sd2neg, label='-2SD', color='red')
    plt.plot(age_months_data, sd0, label='Mean', color='green')
    plt.plot(age_months_data, sd2, label='+2SD', color='red')
    plt.plot(age_months_data, sd3, label='+3SD', color='black')

    # Thêm điểm trọng lượng của trẻ
    plt.scatter(age_months,
                weight,
                color='red',
                label='Child Data Point',
                zorder=5)

    # Thêm tiêu đề và nhãn
    plt.xlabel('Age (months)', fontsize=10)
    plt.ylabel('Weight (kg)', fontsize=10)

    # Chuyển đổi Matplotlib sang Plotly
    plotly_fig = tls.mpl_to_plotly(plt.gcf())
    # Cập nhật hovertemplate (giới hạn số thập phân)
    plotly_fig.update_traces(
        hovertemplate="%{x:.2f}, %{y:.2f}"
    )
    # Cấu hình trục hoành trong Plotly
    plotly_fig.update_xaxes(tickvals=[0, 12, 24, 36, 48, 60],
                            ticktext=[
                                "Birth", "1 year", "2 years", "3 years",
                                "4 years", "5 years"
                            ],
                            range=[0, 61])

    shapes = [
        dict(type="line",
             x0=year * 12,
             y0=sd3neg.min() - 10,
             x1=year * 12,
             y1=sd3.max() + 10,
             line=dict(color="gray",
                       width=0.2,
                       dash="dash"))
        for year in range(1, 6)
    ] + [
        dict(type="line",
             x0=age_months_data.min(),
             y0=y,
             x1=age_months_data.max(),
             y1=y,
             line=dict(color="gray", width=0.2, dash="dash"))
        for y in [5,10,15,20,25]
    ] + [
        dict(type="rect",
             xref="paper",
             yref="paper",
             x0=0,
             y0=0,
             x1=1,
             y1=1,
             line=dict(color="black", width=1))
    ]

    annotations = [
        dict(x=1.001,
             y=sd3neg.iloc[-1],
             text='-3SD',
             font=dict(color='black', size=8, weight='bold'),
             xref="paper",
             yref="y",
             showarrow=False,
             xanchor="left"),
        dict(x=1.001,
             y=sd2neg.iloc[-1],
             text='-2SD',
             font=dict(color='red', size=8, weight='bold'),
             xref="paper",
             yref="y",
             showarrow=False,
             xanchor="left"),
        dict(x=1.001,
             y=sd0.iloc[-1],
             text='Mean',
             font=dict(color='green', size=8, weight='bold'),
             xref="paper",
             yref="y",
             showarrow=False,
             xanchor="left"),
        dict(x=1.001,
             y=sd2.iloc[-1],
             text='+2SD',
             font=dict(color='red', size=8, weight='bold'),
             xref="paper",
             yref="y",
             showarrow=False,
             xanchor="left"),
        dict(x=1.001,
             y=sd3.iloc[-1],
             text='+3SD',
             font=dict(color='black', size=8, weight='bold'),
             xref="paper",
             yref="y",
             showarrow=False,
             xanchor="left")
    ]

    # Cập nhật layout
    plotly_fig.update_layout(autosize=True,
                             width=none,
                             height=none,
                             margin=dict(l=30, r=30, t=20, b=20),
                             annotations=annotations,
                             plot_bgcolor="white",
                             xaxis_title="Age (months)",
                             yaxis_title="Weight (kg)",
                             shapes=shapes)

    # Chuyển đổi biểu đồ thành JSON
    chart_json = plotly_fig.to_json()
    return chart_json

# Hàm vẽ biểu đồ Leng/Height-for-Age (WFA)
def draw_lhfa_chart(adjusted_lenhei, age_months, sex):
     # Lựa chọn dữ liệu theo giới tính
     if sex == 1:  # boys
          file_path = 'data/lhfa-boys-zscore-expanded-tables.xlsx'
     elif sex == 2:  # girls
          file_path = 'data/lhfa-girls-zscore-expanded-tables.xlsx'
     else:
          raise ValueError(
              "Invalid sex. Please use 1 for male or 2 for female.")

     # Đọc dữ liệu từ tệp Excel
     data = pd.read_excel(file_path)

     # Chuyển đổi tuổi từ ngày sang tháng
     age_days = data['Day']
     age_months_data = age_days / 30.4375
     sd3neg = data['SD3neg']
     sd2neg = data['SD2neg']
     sd0 = data['SD0']
     sd2 = data['SD2']
     sd3 = data['SD3']

     # Vẽ biểu đồ bằng Matplotlib
     plt.plot(age_months_data, sd3neg, label='-3SD', color='black')
     plt.plot(age_months_data, sd2neg, label='-2SD', color='red')
     plt.plot(age_months_data, sd0, label='Mean', color='green')
     plt.plot(age_months_data, sd2, label='+2SD', color='red')
     plt.plot(age_months_data, sd3, label='+3SD', color='black')

     # Thêm điểm trọng lượng của trẻ
     plt.scatter(age_months,
                 adjusted_lenhei,
                 color='red',
                 label='Child Data Point',
                 zorder=5)

     # Thêm tiêu đề và nhãn
     plt.xlabel('Lenght/Height (cm)', fontsize=10)
     plt.ylabel('Weight (kg)', fontsize=10)

     # Chuyển đổi Matplotlib sang Plotly
     plotly_fig = tls.mpl_to_plotly(plt.gcf())
     # Cập nhật hovertemplate (giới hạn số thập phân)
     plotly_fig.update_traces(hovertemplate="%{x:.2f}, %{y:.2f}")
     # Cấu hình trục hoành trong Plotly
     plotly_fig.update_xaxes(tickvals=[0, 12, 24, 36, 48, 60],
                             ticktext=[
                                 "Birth", "1 year", "2 years", "3 years",
                                 "4 years", "5 years"
                             ],
                             range=[0, 61])

     shapes = [
         dict(
             type="line",
             x0=year * 12,
             y0=sd3neg.min() - 10,
             x1=year * 12,
             y1=sd3.max() + 10,
             line=dict(
                 color="gray",
                 width=2 if year == 2 else 0.2,  # Nét dày hơn cho year = 2
                 dash="solid" if year == 2 else "dash"  # Nét liền cho year = 2
             )) for year in range(1, 6)
     ] + [
         dict(type="line",
              x0=age_months_data.min(),
              y0=y,
              x1=age_months_data.max(),
              y1=y,
              line=dict(color="gray", width=0.2, dash="dash"))
         for y in [50, 60, 70, 80, 90, 100, 110, 120]
     ] + [
         dict(type="rect",
              xref="paper",
              yref="paper",
              x0=0,
              y0=0,
              x1=1,
              y1=1,
              line=dict(color="black", width=1))
     ]

     annotations = [
         dict(x=1.001,
              y=sd3neg.iloc[-1],
              text='-3SD',
              font=dict(color='black', size=8, weight='bold'),
              xref="paper",
              yref="y",
              showarrow=False,
              xanchor="left"),
         dict(x=1.001,
              y=sd2neg.iloc[-1],
              text='-2SD',
              font=dict(color='red', size=8, weight='bold'),
              xref="paper",
              yref="y",
              showarrow=False,
              xanchor="left"),
         dict(x=1.001,
              y=sd0.iloc[-1],
              text='Mean',
              font=dict(color='green', size=8, weight='bold'),
              xref="paper",
              yref="y",
              showarrow=False,
              xanchor="left"),
         dict(x=1.001,
              y=sd2.iloc[-1],
              text='+2SD',
              font=dict(color='red', size=8, weight='bold'),
              xref="paper",
              yref="y",
              showarrow=False,
              xanchor="left"),
         dict(x=1.001,
              y=sd3.iloc[-1],
              text='+3SD',
              font=dict(color='black', size=8, weight='bold'),
              xref="paper",
              yref="y",
              showarrow=False,
              xanchor="left")
     ]

     # Cập nhật layout
     plotly_fig.update_layout(
         autosize=True,
         margin=dict(l=30, r=30, t=20, b=20),
         annotations=annotations,
         plot_bgcolor="white",
         xaxis_title="Age (months)",
         yaxis_title="Lenght/Height (cm)",
         shapes=shapes,
         width=none,
         height=none, 
     )

     # Chuyển đổi biểu đồ thành JSON
     chart_json = plotly_fig.to_json()
     return chart_json
