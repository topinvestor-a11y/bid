
{ pkgs, ... }:

let
  # requirements.txt에 명시된 라이브러리들을 포함하는 Python 환경을 생성합니다.
  pythonWithPackages = pkgs.python3.withPackages (ps: [
    ps.flask
    ps.pandas
    ps.requests
    ps.beautifulsoup4
    ps.openpyxl
  ]);
in
{
  # 위에서 정의한 Python 환경을 패키지로 사용합니다.
  packages = [
    pythonWithPackages
  ];

  idx = {
    extensions = [
      "ms-python.python"
    ];

    # 이제 pip install을 실행할 필요가 없으므로 workspace 설정을 제거합니다.
    workspace = {};

    # 웹 미리보기 설정을 구성합니다.
    previews = {
      enable = true;
      previews = {
        web = {
          command = ["python" "app.py"];
          manager = "web";
        };
      };
    };
  };
}
