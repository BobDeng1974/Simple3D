#ifndef GL_GLBITMAPWORK_H
#define GL_GLBITMAPWORK_H
#include "head.h"
#include "GLWork.h"
#include "GLProgram.h"
#include "GLTexture.h"
#include "core/GLBmp.h"
#include "utils/GLLock.h"
/*This kind of work run glsl from src to dst, if dst is NULL, then it write result to src*/
class GLBitmapWork:public GLWork
{
    public:
        class Shader:public RefCount
        {
            public:
                Shader(const char* fragSource = NULL);
                ~Shader();
                /*Return mProgram's id*/
                int setUp();
                int use();
                const GLProgram& program() const {return mProgram;}
            private:
                GLProgram mProgram;
        };
        GLBitmapWork(GLBmp* src=NULL, GLBmp* dst=NULL, Shader* shader = NULL);
        virtual ~GLBitmapWork();
        void set(GPPtr<GLBmp> src, GPPtr<GLBmp> dst);

        //Must in GL Thread
        virtual bool onPrepare();
        virtual void onProcess();
        virtual void onFinish();
        virtual void onDestroy();
    protected:
        GPPtr<GLBmp> mSrc;
        GPPtr<GLBmp> mDst;
        GPPtr<GLTexture> mSrcT;
        GPPtr<GLTexture> mDstT;
        GPPtr<Shader> mShader;

        GLLock mLock;
};
#endif
