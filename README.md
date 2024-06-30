# # AOP를 활용한 데이터베이스 백업 데코레이터

현재 Naly 서버에는 데이터베이스 백업을 담당하는 서버가 존재하고, 현재 로직은 데이터 삽입이 일어날 때 백업 API를 호출하는 방식으로 백업된다.

</br></br>

이 방법에는 몇 가지 문제점이 있다.
1. 중복 코드(백업 API 호출 코드)가 많아짐.
2. 트랜잭션(Transcaction)을 고려하지 않음.

</br>

따라서 관점 지향 프로그래밍(AOP, Aspect of Programming)의 개념을 활용하여 백업 API 호출 코드를 정리하여 중복 코드를 줄였다.

</br></br>

또한, 프록시 패턴을 이용하여 함수를 호출하는 프록시 객체를 만들고, 전후로 트랜잭션을 고려한 백업이 가능하도록 처리하였다.

- 데이터 삽입 시, 백업 데이터 저장 (`is_flushed = false`)
- 데이터 삽입 후, 백업 데이터 업데이트 (`is_flushed = true`)

</br></br>

# # 프로젝트 실행하기 

```
python test.py
```

# # 프로젝트에 활용 시 주의할 점 

### 1. `backup.py`에 정의되어 있는 `backup_api` 메소드 구현하기 

백업 서버에 요청을 보내는 함수로, 현재는 프로젝트 하위 `data` 디렉토리에 `json` 형식으로 저장하도록 구현해두었으나, 실제 서비스에서는 `requests`나 `aiohttp` 같은 HTTP 요청 라이브러리로 대체되어야 할 것이다.

### 2. `Backup` 함수 사용법 이해하기 

```python
result = await Backup(
    backup_data={
        "data": test_data
    },
    func=async_external_function,
    args=[test_data]
)
```

- `result` 변수에는 호출하고자 하는 함수(`func`)의 결과값이 들어가게 된다. 
- `backup_data`는 백업 서버에 보낼 데이터를 넣어야 한다. 
  - `data` 필드는 반드시 존재해야 하고, 웬만하면 객체 변형 없이 넣을 수 있도록 하는 것이 좋다.
- `func`는 호출할 함수이다. 
  - 동기, 비동기 함수 모두 정상적으로 동작한다.
- `args`는 호출할 함수에 전달할 인자이다. 인자를 차례대로 리스트 형식으로 넣어준다.

### 3. 백업 결과 이해하기

아래는 백업 데이터 예시이다.

```json
{
    "id": "cC7tDXjrrjCYvtdPyhrYjT3ZIcyBDb",
    "is_flushed": false,
    "time": "2024-06-30T22:09:20.132545",
    "database_id": 0,
    "collection_id": "test",
    "data": {
        "username": "dalmeng",
        "password": "1234"
    }
}
```

- `id`는 백업 데이터에 고유 부여되는 아이디이다.
- `is_flushed`는 데이터베이스에 실제로 반영되었는지 알 수 있는 필드이다.
  - `is_flushed`가 참이면, 데이터베이스에 정상적으로 반영된 상태이다.
  - `is_flushed`가 거짓이면, 사용자가 정상적으로 요청은 했으나, 데이터베이스 서버 문제로 정상적으로 없데이트 되지 못 한 상태이다.
- 따라서 데이터베이스 장애 발생 시, `is_flushed`가 거짓인 데이터를 다시 데이터베이스에 삽입하는 작업이 필요할 것이다.
- `database_id`, `collection_id`는 운영 환경에 따라 변경 가능하다.
- `data`는 실제로 삽입된 데이터이다.

