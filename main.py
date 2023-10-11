import streamlit as st
from fuzzy_logic import FuzzyLogic
import sqlalchemy
from models import *
import matplotlib
import matplotlib.pyplot as plt

st.set_page_config(page_title="BeFit", page_icon="images\\fuzzy.png")

col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([0.5, 0.5, 1, 0.75, 1, 0.75, 0.5, 0.5])

is_first_load = True

with st.sidebar:
    st.title("Параметри тіла")

    if "page1" not in st.session_state:
        st.session_state.page1 = {"is_first_load": True, "sex": 0, "height": 175.0, "weight": 80.0, "stage": 0}

    for k, v in st.session_state.items():
        st.session_state[k] = v

    def submit_sex():
        if st.session_state.sex_input_value == "Чоловік":
            i = 0
        elif st.session_state.sex_input_value == "Жінка":
            i = 1
        st.session_state.page1["sex"] = i  # type: ignore

    def submit_height():
        st.session_state.page1["height"] = st.session_state.height_input_value

    def submit_weight():
        st.session_state.page1["weight"] = st.session_state.weight_input_value

    def submit_stage():
        if st.session_state.stage_input_value == "Так, я початківець":
            st.session_state.page1["stage"] = 0
        elif st.session_state.stage_input_value == "Ні, я маю досвід":
            st.session_state.page1["stage"] = 1

    sex_input = st.radio(
        "**Яка у вас стать?**",
        ("Чоловік", "Жінка"),
        key="sex_input_value",
        index=st.session_state.page1["sex"],
        on_change=submit_sex,
    )

    height_input = st.number_input(
        "**Який у вас ріст (в сантиметрах)?**",
        key="height_input_value",
        min_value=130.0,
        max_value=220.0,
        step=0.1,
        value=st.session_state.page1["height"],
        on_change=submit_height,
    )

    weight_input = st.number_input(
        "**Яка у вас вага (у кілограмах)?**",
        key="weight_input_value",
        min_value=30.0,
        max_value=150.0,
        step=0.1,
        value=st.session_state.page1["weight"],
        on_change=submit_weight,
    )

    stage_input = st.selectbox(
        "**Чи ви уперше на дієті?**",
        ("Так, я початківець", "Ні, я маю досвід"),
        key="stage_input_value",
        index=st.session_state.page1["stage"],
        on_change=submit_stage,
    )

    col1, col2, col3 = st.columns([1, 0.5, 0.85])
    with col1:
        if st.button("Підтвердити"):
            st.session_state.page1["is_first_load"] = False
    with col3:
        if st.button("Скасувати"):
            st.session_state.page1["is_first_load"] = True

if not st.session_state.page1["is_first_load"]:
    fuzzy_logic = FuzzyLogic()
    fuzzy_logic.do_fuzzification_of_height(round(st.session_state.page1["height"], 2), st.session_state.page1["sex"])
    fuzzy_logic.do_fuzzification_of_weight(round(st.session_state.page1["weight"], 2), st.session_state.page1["sex"])
    fuzzy_logic.do_fuzzy_inference()
    body = fuzzy_logic.do_defuzzification_of_body()

    body_result = ""
    match body:
        case 2:
            body_result = "надмірна вага"
        case 3:
            body_result = "можливе ожиріння"
        case 4:
            body_result = "ожиріння"

    if body == 0:
        st.subheader("Ви надто худі! Вам слід набрати ваги!")
    elif body == 1:
        st.subheader("Ви в чудовій формі! Keep going! :sunglasses:")
    else:
        st.subheader(f"У вас {body_result}! Щоб схуднути, слідуйте вказівкам:")

        st.write(
            "**Вуглеводи** (включаючи *цукри*, *крохмаль*, та *целюлозу*) є основним джерелом енергії в людському харчуванні. Щоб схуднути, вам потрібно споживати менше вуглеводів."
        )
        st.markdown(
            """
            У цьому плані харчування, кожен тиждень складається з 3 різних типів днів харчування:
            <ul style="padding-left: 2rem">
            <li><b>Дні з низьким вмістом вуглеводів</b> (менше <b>26%</b> від загальної кількості енергії) - <b>3</b> дні на тиждень</li>
            <li><b>Дні з помірним вмістом вуглеводів</b> (між <b>26%</b> і <b>45%</b> від загальної кількості енергії) - <b>3</b> дні на тиждень</li>
            <li><b>Дні з високим вмістом вуглеводів</b> (більше <b>45%</b> від загальної кількості енергії) - <b>1</b> день на тиждень</li>
            </ul>
            """,
            unsafe_allow_html=True,
        )
        low_carb_1, moderate_carb_1, high_carb_1 = st.columns(3)
        low_carb_2, moderate_carb_2, high_carb_2 = st.columns(3)
        matplotlib.rcParams.update({"font.size": 5})
        label = ["Вуглеводи", "Жири", "Білки"]
        colors = ["#F7D300", "#38BC56", "#D35454"]
        engine = sqlalchemy.create_engine("sqlite:///database/database.db")
        with engine.connect() as conn:
            sc_result = conn.execute(
                sqlalchemy.text("SELECT * FROM StandardCalories WHERE Stage = :stage AND Body = :body AND Sex = :sex"),
                {"stage": st.session_state.page1["stage"], "body": body, "sex": st.session_state.page1["sex"]},
            ).fetchone()
            standard_calories = StandardCalories(*sc_result)  # type: ignore

            lc_result = conn.execute(
                sqlalchemy.text("SELECT * FROM LowCarb WHERE Calories = :calories"),
                {"calories": standard_calories.low_carb},
            ).fetchone()
            low_carb_diet = Diet(*lc_result)  # type: ignore

            low_carb_nutrition_detail = low_carb_diet.get_nutrition_detail()

            low_carb_data = [
                low_carb_nutrition_detail.get_carbs_percentage(),
                low_carb_nutrition_detail.get_fat_percentage(),
                low_carb_nutrition_detail.get_protein_percentage(),
            ]
            low_carb_fig, low_carb_ax = plt.subplots(figsize=(1, 1))
            low_carb_ax.pie(
                low_carb_data,
                labels=label,
                colors=colors,
                explode=(0.15, 0.075, 0.075),
                autopct="%1.1f%%",
                startangle=90,
                wedgeprops={"edgecolor": "black", "linewidth": 1, "antialiased": True},
            )
            low_carb_ax.axis("equal")

            with low_carb_1:
                st.markdown(
                    f"""
                        <h3 style="text-align: center">Дієта з низьким вмістом вуглеводів</h3>
                        <table style="width:100%">
                            <tr>
                                <th style="font-size:18px;">Харчування</th>
                            </tr>
                            <tr>
                                <td>
                                    <b>Calories:</b>
                                    <text style="float:right">{round(low_carb_nutrition_detail.calories)} ккал</text><br/>
                                    <b>Carbs:</b>
                                    <text style="float:right">{low_carb_nutrition_detail.carbs} g</text><br/>
                                    <b>Fat:</b>
                                    <text style="float:right">{low_carb_nutrition_detail.fat} g</text><br/>
                                    <b>Protein:</b>
                                    <text style="float:right">{low_carb_nutrition_detail.protein} g</text><br/>
                                </td>
                            </tr>
                        </table>
                        <br/>
                        <div class="figure_title" style="text-align:center; font-size:20px"><b>Відсоток калорій від:</b></div>
                    """,
                    unsafe_allow_html=True,
                )
                st.pyplot(low_carb_fig)

            lc_result = conn.execute(
                sqlalchemy.text("SELECT * FROM ModerateCarb WHERE Calories = :calories"),
                {"calories": standard_calories.moderate_carb},
            ).fetchone()
            moderate_carb_diet = Diet(*lc_result)  # type: ignore

            moderate_carb_nutrition_detail = moderate_carb_diet.get_nutrition_detail()

            moderate_carb_data = [
                moderate_carb_nutrition_detail.get_carbs_percentage(),
                moderate_carb_nutrition_detail.get_fat_percentage(),
                moderate_carb_nutrition_detail.get_protein_percentage(),
            ]
            moderate_carb_fig, moderate_carb_ax = plt.subplots(figsize=(1, 1))
            moderate_carb_ax.pie(
                moderate_carb_data,
                labels=label,
                colors=colors,
                explode=(0.15, 0.075, 0.075),
                autopct="%1.1f%%",
                startangle=90,
                wedgeprops={"edgecolor": "black", "linewidth": 1, "antialiased": True},
            )
            moderate_carb_ax.axis("equal")

            with moderate_carb_1:
                st.markdown(
                    f"""
                        <h3 style="text-align: center">Дієта з помірним вмістом вуглеводів</h3>
                        <table style="width:100%">
                            <tr>
                                <th style="font-size:18px;">Харчування</th>
                            </tr>
                            <tr>
                                <td>
                                    <b>Calories:</b>
                                    <text style="float:right">{round(moderate_carb_nutrition_detail.calories)} ккал</text><br/>
                                    <b>Carbs:</b>
                                    <text style="float:right">{moderate_carb_nutrition_detail.carbs} g</text><br/>
                                    <b>Fat:</b>
                                    <text style="float:right">{moderate_carb_nutrition_detail.fat} g</text><br/>
                                    <b>Protein:</b>
                                    <text style="float:right">{moderate_carb_nutrition_detail.protein} g</text><br/>
                                </td>
                            </tr>
                        </table>
                        <br/>
                        <div class="figure_title" style="text-align:center; font-size:20px"><b>Відсоток калорій від:</b></div>
                    """,
                    unsafe_allow_html=True,
                )
                st.pyplot(moderate_carb_fig)
            # Get high carb diet
            hc_result = conn.execute(
                sqlalchemy.text("SELECT * FROM HighCarb WHERE Calories = :calories"),
                {"calories": standard_calories.high_carb},
            ).fetchone()
            high_carb_diet = Diet(*hc_result)  # type: ignore

            high_carb_nutrition_detail = high_carb_diet.get_nutrition_detail()

            high_carb_data = [
                high_carb_nutrition_detail.get_carbs_percentage(),
                high_carb_nutrition_detail.get_fat_percentage(),
                high_carb_nutrition_detail.get_protein_percentage(),
            ]
            high_carb_fig, high_carb_ax = plt.subplots(figsize=(1, 1))
            high_carb_ax.pie(
                high_carb_data,
                labels=label,
                colors=colors,
                explode=(0.15, 0.075, 0.075),
                autopct="%1.1f%%",
                startangle=90,
                wedgeprops={"edgecolor": "black", "linewidth": 1, "antialiased": True},
            )
            high_carb_ax.axis("equal")

            with high_carb_1:
                st.markdown(
                    f"""
                        <h3 style="text-align: center">Дієта з високим вмістом вуглеводів</h3>
                        <table style="width:100%">
                            <tr>
                                <th style="font-size:18px;">Харчування</th>
                            </tr>
                            <tr>
                                <td>
                                    <b>Calories:</b>
                                    <text style="float:right">{round(high_carb_nutrition_detail.calories)} ккал</text><br/>
                                    <b>Carbs:</b>
                                    <text style="float:right">{high_carb_nutrition_detail.carbs} g</text><br/>
                                    <b>Fat:</b>
                                    <text style="float:right">{high_carb_nutrition_detail.fat} g</text><br/>
                                    <b>Protein:</b>
                                    <text style="float:right">{high_carb_nutrition_detail.protein} g</text><br/>
                                </td>
                            </tr>
                        </table>
                        <br/>
                        <div class="figure_title" style="text-align:center; font-size:20px"><b>Відсоток калорій від:</b></div>
                    """,
                    unsafe_allow_html=True,
                )
                st.pyplot(high_carb_fig)

        st.write(
            "Рекомендуємо залишати високовуглеводний день для особливих випадків, таких як родинні заходи або поїздки з друзями."
        )
