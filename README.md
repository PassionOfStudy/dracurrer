# dracurrer
드라마 + 큐레이션 프로젝트

<h2 align="center"> 제작기간 및 팀원 소개 </h2>
<p align="center"> 2022. 03. 07 ~2022. 03.10 </p>
<p> 
    <code>박태순</code> : 로그인,회원가입 페이지 <br />
    <code>임차혁</code> : 메인, 등록 페이지 <br />
    <code>이진혁</code> : 리뷰 페이지 <br />
</p>

<h2 align="center"> ✔사용한 기술</h2>

<h4>- 언어</h4>
<p float="left">
<img src="https://img.shields.io/badge/html5-E34F26?style=for-the-badge&logo=html5&logoColor=white">
<img src="https://img.shields.io/badge/CSS-1572B6?style=for-the-badge&logo=CSS&logoColor=white">
<img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=JavaScript&logoColor=white">
<img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54">
</p>

<h4>-프레임워크 / 플랫폼 / 라이브러리</h4>
<p float="left">
<img src="https://img.shields.io/badge/jquery-%230769AD.svg?style=for-the-badge&logo=jquery&logoColor=white">
<img src="https://img.shields.io/badge/bootstrap-%23563D7C.svg?style=for-the-badge&logo=bootstrap&logoColor=white">
<img src="https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens">
<img src="https://img.shields.io/badge/Jinja-7952B3?style=for-the-badge&logo=Jinja&logoColor=white">
<img src="https://img.shields.io/badge/Flask-00ffff?style=for-the-badge&logo=Flask&logoColor=black">
</p>

<h4>-에디터</h4>
<img src="https://img.shields.io/badge/pycharm-143?style=for-the-badge&logo=pycharm&logoColor=black&color=black&labelColor=brightgreen">

<h4>-협업툴</h4>
<p float="left">
<img src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white">
<img src="https://img.shields.io/badge/git-F05032?style=for-the-badge&logo=git&logoColor=white">
</p>
<h4>-데이터베이스</h4>
<img src="https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white">

<h4>-호스팅<h4>
<img src="https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white">

<h2 align="center"> ✔ 필수 요구 사항  </h2>
<h4>jinja2 템플릿 엔진을 이용한 서버사이드 렌더링 </h4>
<p>: 서버사이드렌더링(SSR)을 사용하면 모든 데이터가 매핑된 서비스 페이지를 클라이언트(브라우저)에게 바로 보여줄 수 있다.<br />서버를 이용해 페이지를 구성하기 때문에 클라이언트 사이드 렌더링(CSR)보다 페이지 구성 속도는 느리지만 전체적으로 사용자에게 보여주는 컨텐츠 구성이 완료되는 시점은 빨라진다는 장점이 있다.<br />
또한 SEO도 쉽게 구성할 수 있다.
<h4>JWT 인증 방식으로 로그인 구현하기 </h4>
<p>: JWT는 Json Web Token의 약자로 인증에 필요한 정보를 암호화시킨 토큰을 뜻한다. <br />
JWT인증방식은 인증받은 사용자에게 토큰을 발급해주고, <br />
서버에 서버에 요청을 할 때 HTTP 헤더에 토큰을 함께 보내 인증받은 사용자(유효성 검사)인지 확인한다.<br />
쿠키를 사용함으로 인해 발생하는 취약점이 사라지며 서버 기반 인증 시스템은 저장소의 관리가 필요하지만, <br />
토큰 기반은 Access Token을 발급해준 후 요청이 들어오면 검증만 해주면 되기 때문에 추가 저장소가 필요 없다.</p>
