import os
import pyperclip
from datetime import datetime
from .api import api_request
from .utils import sort_folders_by_md_file_count as sort_folders


class TodoMaker:
    def __init__(self, OBSIDIAN_DIR):
        self.persons = None
        self.selectedPerson = None
        self.topClassName = None
        self.subClassName = None
        self.subDivisionName = None
        self.complete_dir = None
        self.fileName = None
        self.todayDate = datetime.now().strftime("%Y-%m-%d")
        self.dateDirName = datetime.now().strftime("%Y%m") + "_"
        self.todayYear = datetime.now().strftime("%Y")
        self.FIELD = sort_folders(OBSIDIAN_DIR)
        self.OBSIDIAN_DIR = OBSIDIAN_DIR

    def show_person_info(self, persons: list) -> None:
        print()
        for i, person in enumerate(persons):
            buseo_nm = person['buseo_nm']
            username = person['username']
            gyonae_no = self.conv_call(person['gyonae_no'])
            jikwi = person['jikwi']
            chrg_busns_nm = person['chrg_busns_nm']
            print(
                f"[{i+1:02d}] {buseo_nm}\t{username}\t{gyonae_no}\t{jikwi} / {chrg_busns_nm}")

    def conv_call(self, val: str) -> str:
        """
        Convert a contact number to a simplified form.

        Args:
            val (str): The contact number to be converted.

        Returns:
            str: The simplified contact number.

        Example:
            - Input: "043-230-3346"
            - Output: "3346"
        """
        return val.split('-')[-1] if val else ""

    def selectPerson(self) -> None:
        """
        Select a faculty or staff member from the information retrieved through apiCall and store it in self.selectedPerson.

        This function allows the user to choose a specific person from the list of faculty and staff information obtained through apiCall.

        Returns:
            None
        """
        while True:
            tmp = input("검색어를 입력해주세요: ").strip()
            if not tmp:
                continue

            self.persons = api_request(tmp)
            if self.persons['cnt'] == 0:
                print("검색된 데이터가 없습니다. 다시 진행해주세요.")
                continue

            if self.persons['cnt'] == 1:
                print('검색된 데이터가 1개입니다. 자동으로 선택됩니다.')
                self.selectedPerson = self.persons['data'][0]

                print(
                    f"{self.selectedPerson['buseo_nm']}\t{self.selectedPerson['username']}\t{self.conv_call(self.selectedPerson['gyonae_no'])}\t{self.selectedPerson['jikwi']} / {self.selectedPerson['chrg_busns_nm']}\n")
                break

            self.show_person_info(self.persons['data'])

            target = int(input("대상자를 선택해주세요.(다시 검색하려면 0): "))
            if target == 0:
                continue

            self.selectedPerson = self.persons['data'][target - 1]
            break

    def topClass(self) -> None:
        """
        Select your primary field of work.

        This function allows you to choose your primary area of work or specialization.

        Returns:
            None
        """
        for i, f in enumerate(self.FIELD):
            print(f"[{i:02d}] {f}")

        self.topClassName = self.FIELD[int(input("\n업무 분야를 선택해주세요: "))]

    def subclass(self) -> None:
        """
        하위 업무 분야를 선택합니다.
        """
        if self.topClassName is None:
            print("상위 분야를 먼저 선택해주세요.")
            return

        try:
            subDir = sort_folders(os.path.join(
                self.OBSIDIAN_DIR, self.topClassName))
        except FileNotFoundError:
            subDir = []

        for i, f in enumerate(subDir):
            print(f"[{i:02d}] {f}")

        tmp = input("\n하위 분야를 선택해주세요(만약 없으면 하위 분야 입력): ").strip()

        if tmp.isdigit():
            self.subClassName = subDir[int(tmp)]
        else:
            self.subClassName = tmp

    def makeSubDivision(self):
        self.subDivisionName = input("단위 업무를 입력해주세요: ").strip()
        self.complete_dir = os.path.join(self.OBSIDIAN_DIR, self.topClassName, self.subClassName,
                                         self.todayYear, self.dateDirName + self.subDivisionName)

    def makeTodoMD(self):
        """
        .md 파일을 생성합니다.
        """
        contents = []
        contents.extend([
            "---",
            f"tag: 업무/{self.topClassName}/{self.subClassName} 부서/{
                self.selectedPerson['buseo_nm']}",
            "---",
            "",
            f"# {self.subDivisionName}",
            "",
            "## 🙋‍♂️ 관련",
            f"- [[{self.selectedPerson['username']}({self.selectedPerson['userId']})]] #부서/{self.selectedPerson['buseo_nm']}/{
                self.selectedPerson['jikwi']}_{self.selectedPerson['username']} - {self.conv_call(self.selectedPerson['gyonae_no'])}",
            "",
            "## 📢 내용",
        ])

        while True:
            tmp = input("내용: ").strip()
            if not tmp:
                break
            contents.append(f"- {tmp}")

        contents.extend([
            "",
            "## 🛠 조치",
        ])

        while True:
            tmp = input("조치: ").strip()
            if not tmp:
                break
            contents.append(
                f"- [ ] {tmp} ➕ {self.todayDate} 📅 {self.todayDate}")

        contents.extend([
            "",
            "## 📂 정보",
            "- ",
            "",
            "## 🏷 연관",
            "- ",
            "",
            "## 🔔개선점",
            "- ",
        ])

        return "\n".join(contents)

    def makeTodoFile(self):
        """
        지금까지 입력된 정보를 기반으로 폴더 및 .md 파일을 생성합니다.
        """
        mdContents = self.makeTodoMD()

        os.makedirs(self.complete_dir, exist_ok=True)

        self.fileName = os.path.join(
            self.complete_dir, f"_{self.subDivisionName}.md")
        with open(self.fileName, "w", encoding="UTF-8") as f:
            f.write(mdContents)

    def copy_to_clipboard(self):
        """
        Copy the folder path of the generated .md file to the clipboard.
        """
        pyperclip.copy(self.complete_dir)

    def run(self):
        self.selectPerson()         # 관련자 선택
        self.topClass()             # 최상위 업무 단위 선택
        self.subclass()             # 하위 업무 단위 선택 or 입력
        self.makeSubDivision()      # 업무별 제목 입력
        self.makeTodoFile()         # 실제 파일 생성
        self.copy_to_clipboard()    # 폴더 경로 클립보드에 복사
