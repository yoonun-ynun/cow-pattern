from database.info import Info
from database.database import Database
from compare.compare import Compare
from extraction.extraction import Extraction
import tkinter as tk
from tkinter import filedialog

extra = Extraction()
comp = Compare()
info = Info()
db = Database()

idNum = 0

def inputImage() : #tkinter로 이미지를 입력 받는다.
    file_path = filedialog.askopenfilename(
        title = "이미지 선택", 
        filetypes=[("이미지 파일", "*.png; *.jpg; *jpeg")])
    return file_path #이미지의 경로를 반환

def printCowList(infoList) : #소 info 리스트를 받아 출력
    print("ID\t소유자")
    for info in infoList :
        print(f"{info.id}\t{info.name}")

while(1) :
    cmd = int(input("사용할 명령을 입력하세요.\n"
            "(등록: 1, 조회: 2, 수정: 3, 삭제: 4, 종료: 5) -> "))

    if(cmd == 1) : #소 정보 등록
        file_path = inputImage() #이미지 경로 가져옴
        if(file_path) : #사용자가 취소하여 경로가 없는지 확인
            vector = extra.feature(file_path) #이미지 벡터 값 가져옴
        else : #없다면 처음으로 돌아감
            print("취소되었습니다.")
            print()
            continue

        if(comp.check(vector) == None) : #DB에 해당 벡터 값이 없다면 
            userName = input("소유자 이름을 입력하세요. -> ")
            info.__init__(idNum, userName, vector)
            idNum += 1 # ID는 순차적으로 증가
            db.create(info)
            print("등록이 완료되었습니다.")
        else :
            print("이미 등록된 소 입니다.")

    elif(cmd == 2) : #정보 조회
        #이미지 입력과 소유자 입력 선택
        inpWay = int(input("비문 이미지로 조회하기 : 1\n"
                            "소유자 이름으로 조회하기 : 2 -> "))
        
        if(inpWay == 1) : #이미지 입력 동작
            file_path = inputImage()
            vector = extra.feature(file_path)
            cowId = comp.check(vector) #해당 이미지의 소 ID 가져옴

            if(cowId != None) : 
                info = db.get_by_id(cowId) #ID로 소 info 가져옴
                infoList = [info] #함수에 넣기 위해 리스트에 넣음
                printCowList(infoList) #소 정보 출력
            else :
                print("등록되어 있지 않은 소입니다.")

        elif(inpWay == 2) : #소유자 이름 입력 동작
            userName = input("소유자 이름을 입력하세요. -> ")
            infoList = db.get_by_user(userName)
            printCowList(infoList)

        else :
            print("올바른 입력 방법이 아닙니다.")

    elif(cmd == 3) : #정보 수정
        cowId = input("갱신할 정보의 소 ID를 입력하세요. -> ")
        preInfo = db.get_by_id(cowId) #변경하지 않을 값을 임시저장

        userName = input("변경할 사용자 이름을 입력하세요 -> ")
        #ID, 벡터는 변경 X, 소유자 이름만 변경
        info.__init__(preInfo.id, userName, preInfo.vector)

        if(db.update(cowId, info)) :
            print("정보 변경이 완료되었습니다.")
        else :
            print("정보를 변경할 수 없습니다.")

    elif(cmd == 4) : #정보삭제
        cowId = input("삭제할 소의 ID를 입력하세요. -> ")
        if(db.delete(cowId)) :
            print("성공적으로 삭제 되었습니다.")
        else :
            print("삭제할 수 없습니다.")

    elif(cmd == 5) :
        print("종료합니다.")
        break
    else :
        print("올바른 명령이 아닙니다.")
    print()
            
            
            