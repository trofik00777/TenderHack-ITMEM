class Recommender:
    def __init__(self, sessions, our_min):
        self.our_min = our_min
        self.curr_sessions = {}
        for key in sessions:
            self.curr_sessions[key] = self.get_cost_for_session(sessions[key])
        self.curr_sessions = list(self.curr_sessions.items())
        self.curr_sessions.sort(key=self.sort_by_cost, reverse=True)
        print(self.curr_sessions)

    def get_cost_for_session(self, session):
        return session['last_price'] / self.our_min - session['cnt_players'] / 1000 - session['time'] / 1000

    @staticmethod
    def sort_by_cost(elem):
        return elem[1]