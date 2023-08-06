class Machine:
    def __init__(self, client):
        self.client = client

    def list_machine_by_page(self, cpu_only=True, platform=None, page=1, per_page=30):
        params = {'page': page, 'per_page': per_page, "type": "all"}
        if platform is not None:
            params['platform'] = platform
        if cpu_only:
            params['gpu'] = "cpu"
        data = self.client.get('/resources/instances', params=params)
        return data

    def list_all_machine(self, cpu_only=False, platform=None):
        program_list = []
        data = self.list_machine_by_page(cpu_only=cpu_only, platform=platform)
        total = data['total']
        per_page = data['per_page']
        page_number = 0
        while page_number * per_page < total:
            page_number = page_number + 1
            if page_number > 1:
                data = self.list_machine_by_page(cpu_only=cpu_only, platform=platform, page=page_number, per_page=30)
            program_list.extend(data['items'])
        return program_list
