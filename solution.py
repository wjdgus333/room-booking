# 강의실 예약 시스템 — 아래 클래스를 완성하세요. (클래스·메서드 이름은 바꾸지 마세요)

ROOMS = ("A101", "A102", "B201")
DAYS = ("월", "화", "수", "목", "금")
OPEN_HOUR = 9
CLOSE_HOUR = 21
MAX_HOURS = 3
MAX_PER_PERSON_PER_DAY = 2


def _is_int(value):
    # bool은 int의 하위 타입이므로 따로 제외
    return isinstance(value, int) and not isinstance(value, bool)


def _valid_place(room, day):
    return isinstance(room, str) and isinstance(day, str) and room in ROOMS and day in DAYS


class RoomBooking:
    def __init__(self):
        # (room, day) -> [(start, end, name), ...]
        self._bookings = {(room, day): [] for room in ROOMS for day in DAYS}

    def book(self, room, day, start, end, name):
        # 1. 강의실·요일
        if not _valid_place(room, day):
            return False
        # 2. 정수 시각
        if not _is_int(start) or not _is_int(end):
            return False
        # 3. 운영 시간
        if start < OPEN_HOUR or end > CLOSE_HOUR:
            return False
        # 4. 시작 < 끝
        if start >= end:
            return False
        # 5. 3시간 초과 금지
        if end - start > MAX_HOURS:
            return False
        # 6. 같은 강의실·요일 시간 겹침 (끝나는 시각에 바로 시작은 허용)
        for s, e, _ in self._bookings[(room, day)]:
            if start < e and s < end:
                return False
        # 7. 같은 사람은 같은 요일에 최대 2건 (강의실 합산)
        count = 0
        for r in ROOMS:
            for _, _, n in self._bookings[(r, day)]:
                if n == name:
                    count += 1
        if count >= MAX_PER_PERSON_PER_DAY:
            return False

        self._bookings[(room, day)].append((start, end, name))
        return True

    def cancel(self, room, day, start, name):
        if not _valid_place(room, day) or not _is_int(start):
            return False
        bookings = self._bookings[(room, day)]
        for i, (s, _, n) in enumerate(bookings):
            if s == start:
                if n != name:
                    return False
                del bookings[i]
                return True
        return False

    def get_schedule(self, room, day):
        if not _valid_place(room, day):
            return []
        return sorted(self._bookings[(room, day)], key=lambda b: b[0])
