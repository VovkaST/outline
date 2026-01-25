import {
  OpenAPI,
  TasksService
} from '@/api/generated/public';
import { getEnvVar } from '@/config/utils';
import { defineStore } from 'pinia';

if (import.meta.env.DEV) {
  OpenAPI.BASE = getEnvVar("VITE_BASE_URL", 'http://127.0.0.1:8000');
}

export const useTasksStore = defineStore('TasksStore', {
  actions: {
    createTask() {
      return TasksService.create();
    },

    getTaskKey({taskId}: {taskId: number}) {
      return TasksService.getTaskKey({taskId: String(taskId)});
    },
  },
});
